import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import stockService from "@/services/stockService";
import type { StockCreate, StockUpdate, StockFilters } from "@/types/stock";

export function useProjectStock(projectId: number, filters?: StockFilters) {
  return useQuery({
    queryKey: ["stock", projectId, filters],
    queryFn: () => stockService.getByProject(projectId, filters),
    enabled: projectId > 0,
  });
}

export function useStockUnit(id: number) {
  return useQuery({
    queryKey: ["stock", "unit", id],
    queryFn: () => stockService.getById(id),
    enabled: id > 0,
  });
}

export function useCreateStock() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: StockCreate) => stockService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

export function useUpdateStock() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: StockUpdate }) =>
      stockService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

export function useDeleteStock() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => stockService.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}
