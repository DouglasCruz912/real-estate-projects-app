import api from "@/services/api";
import type {
  StockUnit,
  StockCreate,
  StockUpdate,
  StockFilters,
  StockListResponse,
} from "@/types/stock";

const stockService = {
  getByProject(
    projectId: number,
    params?: StockFilters
  ): Promise<StockListResponse> {
    return api
      .get(`/api/stock/project/${projectId}`, { params })
      .then((res) => res.data);
  },

  getById(id: number): Promise<StockUnit> {
    return api.get(`/api/stock/${id}`).then((res) => res.data);
  },

  create(data: StockCreate, brokerEmail: string): Promise<StockUnit> {
    return api
      .post("/api/stock", data, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },

  update(
    id: number,
    data: StockUpdate,
    brokerEmail: string
  ): Promise<StockUnit> {
    return api
      .put(`/api/stock/${id}`, data, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },

  remove(id: number, brokerEmail: string): Promise<void> {
    return api
      .delete(`/api/stock/${id}`, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },
};

export default stockService;
