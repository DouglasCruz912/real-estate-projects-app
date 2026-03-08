import api from "@/services/api";
import type {
  Company,
  CompanyCreate,
  CompanyUpdate,
  CompanyFilters,
} from "@/types/company";

const companyService = {
  getAll(params?: CompanyFilters): Promise<Company[]> {
    return api.get("/api/companies", { params }).then((res) => res.data);
  },

  getById(id: number): Promise<Company> {
    return api.get(`/api/companies/${id}`).then((res) => res.data);
  },

  create(data: CompanyCreate, brokerEmail: string): Promise<Company> {
    return api
      .post("/api/companies", data, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },

  update(
    id: number,
    data: CompanyUpdate,
    brokerEmail: string
  ): Promise<Company> {
    return api
      .put(`/api/companies/${id}`, data, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },

  remove(id: number, brokerEmail: string): Promise<void> {
    return api
      .delete(`/api/companies/${id}`, {
        params: { broker_email: brokerEmail },
      })
      .then((res) => res.data);
  },
};

export default companyService;
