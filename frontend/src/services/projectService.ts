import api from "@/services/api";
import type {
  Project,
  ProjectCreate,
  ProjectUpdate,
  ProjectFilters,
  ProjectListResponse,
} from "@/types/project";

const projectService = {
  getAll(params?: ProjectFilters): Promise<ProjectListResponse> {
    return api.get("/api/projects", { params }).then((res) => res.data);
  },

  getById(id: number): Promise<Project> {
    return api.get(`/api/projects/${id}`).then((res) => res.data);
  },

  getDetails(id: number): Promise<Project> {
    return api.get(`/api/projects/${id}/details`).then((res) => res.data);
  },

  create(data: ProjectCreate): Promise<Project> {
    return api.post("/api/projects", data).then((res) => res.data);
  },

  update(id: number, data: ProjectUpdate): Promise<Project> {
    return api.put(`/api/projects/${id}`, data).then((res) => res.data);
  },

  remove(id: number): Promise<void> {
    return api.delete(`/api/projects/${id}`).then((res) => res.data);
  },
};

export default projectService;
