import api from "@/services/api";

export interface UserData {
  id: number;
  full_name: string;
  email: string;
  phone: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreateData {
  full_name: string;
  email: string;
  password: string;
  phone?: string;
  role?: string;
}

export interface UserUpdateData {
  full_name?: string;
  email?: string;
  phone?: string;
  role?: string;
  is_active?: boolean;
  password?: string;
}

const userService = {
  getAll(): Promise<UserData[]> {
    return api.get("/api/users").then((res) => res.data);
  },

  getById(id: number): Promise<UserData> {
    return api.get(`/api/users/${id}`).then((res) => res.data);
  },

  create(data: UserCreateData): Promise<UserData> {
    return api.post("/api/users", data).then((res) => res.data);
  },

  update(id: number, data: UserUpdateData): Promise<UserData> {
    return api.put(`/api/users/${id}`, data).then((res) => res.data);
  },

  remove(id: number): Promise<void> {
    return api.delete(`/api/users/${id}`).then((res) => res.data);
  },
};

export default userService;
