import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import projectService from "@/services/projectService";
import type {
  ProjectCreate,
  ProjectUpdate,
  ProjectFilters,
} from "@/types/project";

const brokerEmail = process.env.NEXT_PUBLIC_BROKER_EMAIL || "";

export function useProjects(filters?: ProjectFilters) {
  return useQuery({
    queryKey: ["projects", filters],
    queryFn: () => projectService.getAll(filters),
  });
}

export function useProject(id: number) {
  return useQuery({
    queryKey: ["projects", id],
    queryFn: () => projectService.getById(id),
    enabled: id > 0,
  });
}

export function useCreateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ProjectCreate) =>
      projectService.create(data, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}

export function useUpdateProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProjectUpdate }) =>
      projectService.update(id, data, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}

export function useDeleteProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => projectService.remove(id, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
}
