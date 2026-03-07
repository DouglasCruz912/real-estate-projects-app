"""
Servicio S3 para manejo de imágenes y documentos
Configurado para trabajar con AWS S3 bucket-api-projects
"""

import os
import boto3
import uuid
import mimetypes
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, UploadFile
from botocore.exceptions import ClientError, NoCredentialsError
import structlog

logger = structlog.get_logger()


class S3Service:
    """Servicio para gestionar archivos en AWS S3"""
    
    def __init__(self):
        """Inicializar cliente S3"""
        try:
            # Configurar cliente S3 con credenciales específicas
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY'),
                aws_secret_access_key=os.environ.get('AWS_S3_SECRET_KEY'),
                region_name=os.environ.get('AWS_S3_REGION', 'us-west-2')
            )
            
            # Configurar bucket único
            self.bucket_name = os.environ.get('AWS_S3_BUCKET_NAME', 'bucket-api-projects')
            
            # Configurar región
            self.region = os.environ.get('AWS_S3_REGION', 'us-west-2')
            
            # Configurar carpetas base
            self.images_folder = "images"
            self.documents_folder = "documents"
            
            logger.info("✅ S3 Service inicializado", 
                       bucket=self.bucket_name,
                       region=self.region,
                       images_folder=self.images_folder,
                       documents_folder=self.documents_folder)
                       
        except NoCredentialsError:
            logger.error("❌ Credenciales AWS no encontradas")
            raise HTTPException(status_code=500, detail="AWS credentials not configured")
        except Exception as e:
            logger.error("❌ Error inicializando S3 Service", error=str(e))
            raise HTTPException(status_code=500, detail=f"S3 initialization error: {str(e)}")
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generar nombre único para archivo"""
        file_extension = original_filename.split('.')[-1] if '.' in original_filename else 'bin'
        unique_id = str(uuid.uuid4())
        return f"{unique_id}.{file_extension}"
    
    def _get_content_type(self, filename: str) -> str:
        """Obtener tipo de contenido basado en extensión"""
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or 'application/octet-stream'
    
    def _get_folder_for_file_type(self, file_type: str) -> str:
        """Obtener carpeta apropiada según tipo de archivo"""
        if file_type in ['image', 'img']:
            return self.images_folder
        elif file_type in ['document', 'doc']:
            return self.documents_folder
        else:
            return self.images_folder  # Default
    
    async def upload_file(
        self, 
        file: UploadFile, 
        file_type: str = "image",
        project_id: Optional[int] = None,
        folder: str = ""
    ) -> Dict[str, Any]:
        """
        Subir archivo a S3
        
        Args:
            file: Archivo a subir
            file_type: Tipo de archivo ('image', 'document')
            project_id: ID del proyecto (opcional)
            folder: Carpeta adicional (opcional)
            
        Returns:
            Dict con información del archivo subido
        """
        try:
            # Validar archivo
            if not file.filename:
                raise HTTPException(status_code=400, detail="Filename is required")
            
            # Leer contenido del archivo
            content = await file.read()
            
            # Generar nombre único
            unique_filename = self._generate_unique_filename(file.filename)
            
            # Construir key del objeto con la carpeta correcta
            key_parts = [self._get_folder_for_file_type(file_type)]  # Carpeta base (images/ o documents/)
            
            if folder and folder != self._get_folder_for_file_type(file_type):
                key_parts.append(folder)
            if project_id:
                key_parts.append(f"project_{project_id}")
            
            key_parts.append(unique_filename)
            
            object_key = "/".join(key_parts)
            
            # Configurar metadata
            metadata = {
                'original-filename': file.filename,
                'content-type': file.content_type or self._get_content_type(file.filename),
                'file-type': file_type
            }
            
            if project_id:
                metadata['project-id'] = str(project_id)
            
            # Subir archivo a S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=content,
                ContentType=file.content_type or self._get_content_type(file.filename),
                Metadata=metadata,
                ServerSideEncryption='AES256'  # Encriptación
            )
            
            # Generar URL pública
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_key}"
            
            result = {
                "success": True,
                "filename": unique_filename,
                "original_filename": file.filename,
                "bucket": self.bucket_name,
                "key": object_key,
                "url": file_url,
                "size": len(content),
                "content_type": file.content_type or self._get_content_type(file.filename),
                "file_type": file_type
            }
            
            logger.info("✅ Archivo subido a S3", 
                       filename=unique_filename,
                       bucket=self.bucket_name,
                       key=object_key,
                       size=len(content))
            
            return result
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            logger.error("❌ Error S3 ClientError", 
                        error_code=error_code,
                        filename=file.filename)
            raise HTTPException(status_code=500, detail=f"S3 error: {error_code}")
        
        except Exception as e:
            logger.error("❌ Error subiendo archivo", 
                        error=str(e),
                        filename=file.filename)
            raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")
    
    async def delete_file(self, object_key: str) -> bool:
        """
        Eliminar archivo de S3
        
        Args:
            object_key: Key del objeto en S3
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            logger.info("✅ Archivo eliminado de S3", 
                       bucket=self.bucket_name,
                       key=object_key)
            
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            logger.error("❌ Error eliminando de S3", 
                        error_code=error_code,
                        bucket=self.bucket_name,
                        key=object_key)
            return False
        
        except Exception as e:
            logger.error("❌ Error eliminando archivo", 
                        error=str(e),
                        bucket=self.bucket_name,
                        key=object_key)
            return False
    
    async def get_file_info(self, object_key: str) -> Dict[str, Any]:
        """
        Obtener información de archivo en S3
        
        Args:
            object_key: Key del objeto en S3
            
        Returns:
            Dict con información del archivo
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            return {
                "exists": True,
                "size": response.get('ContentLength', 0),
                "last_modified": response.get('LastModified'),
                "content_type": response.get('ContentType'),
                "metadata": response.get('Metadata', {}),
                "url": f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_key}"
            }
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return {"exists": False}
            raise
    
    async def list_project_files(
        self, 
        project_id: int, 
        file_type: str = "image",
        folder: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Listar archivos de un proyecto
        
        Args:
            project_id: ID del proyecto
            file_type: Tipo de archivo
            folder: Carpeta específica
            
        Returns:
            Lista de archivos del proyecto
        """
        try:
            # Construir prefix con la carpeta correcta
            prefix_parts = [self._get_folder_for_file_type(file_type)]
            
            if folder:
                prefix_parts.append(folder)
            prefix_parts.append(f"project_{project_id}")
            prefix = "/".join(prefix_parts) + "/"
            
            # Listar objetos
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            for obj in response.get('Contents', []):
                file_info = {
                    "key": obj['Key'],
                    "filename": obj['Key'].split('/')[-1],
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'],
                    "url": f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{obj['Key']}"
                }
                files.append(file_info)
            
            return files
            
        except Exception as e:
            logger.error("❌ Error listando archivos", 
                        error=str(e),
                        project_id=project_id)
            return []
    
    async def generate_presigned_url(
        self, 
        object_key: str, 
        expiration: int = 3600
    ) -> str:
        """
        Generar URL firmada para acceso temporal
        
        Args:
            object_key: Key del objeto
            expiration: Tiempo de expiración en segundos
            
        Returns:
            URL firmada
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            
            return url
            
        except Exception as e:
            logger.error("❌ Error generando URL firmada", 
                        error=str(e),
                        bucket=self.bucket_name,
                        key=object_key)
            raise HTTPException(status_code=500, detail=f"Presigned URL error: {str(e)}")


# Instancia global del servicio
s3_service = S3Service()


# Funciones de conveniencia
async def upload_image(file: UploadFile, project_id: Optional[int] = None) -> Dict[str, Any]:
    """Subir imagen a S3"""
    return await s3_service.upload_file(file, "image", project_id)


async def upload_document(file: UploadFile, project_id: Optional[int] = None) -> Dict[str, Any]:
    """Subir documento a S3"""
    return await s3_service.upload_file(file, "document", project_id)


async def delete_file_from_s3(key: str) -> bool:
    """Eliminar archivo de S3"""
    return await s3_service.delete_file(key) 