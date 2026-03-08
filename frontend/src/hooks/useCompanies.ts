import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import companyService from "@/services/companyService";
import type {
  CompanyCreate,
  CompanyUpdate,
  CompanyFilters,
} from "@/types/company";

const brokerEmail = process.env.NEXT_PUBLIC_BROKER_EMAIL || "";

export function useCompanies(filters?: CompanyFilters) {
  return useQuery({
    queryKey: ["companies", filters],
    queryFn: () => companyService.getAll(filters),
  });
}

export function useCompany(id: number) {
  return useQuery({
    queryKey: ["companies", id],
    queryFn: () => companyService.getById(id),
    enabled: id > 0,
  });
}

export function useCreateCompany() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CompanyCreate) =>
      companyService.create(data, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
    },
  });
}

export function useUpdateCompany() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: CompanyUpdate }) =>
      companyService.update(id, data, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
    },
  });
}

export function useDeleteCompany() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => companyService.remove(id, brokerEmail),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
    },
  });
}
