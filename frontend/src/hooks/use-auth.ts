/**
 * Shared authentication hook.
 *
 * Centralizes token storage/retrieval and user state
 * so auth logic isn't duplicated across pages.
 */

"use client";

import { useCallback, useEffect, useState } from "react";

import { apiClient } from "@/lib/api-client";
import type { ApiResponse, User } from "@/types/api";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    loading: true,
  });

  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    if (token) {
      setState((s) => ({ ...s, isAuthenticated: true, loading: false }));
    } else {
      setState((s) => ({ ...s, loading: false }));
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await apiClient.post<ApiResponse<{ token: string; user_id: number }>>(
      "/auth/login",
      { email, password }
    );
    localStorage.setItem("auth_token", res.data.token);
    setState({ user: null, isAuthenticated: true, loading: false });
    return res.data;
  }, []);

  const register = useCallback(
    async (email: string, password: string, fullName: string) => {
      const res = await apiClient.post<ApiResponse<{ token: string; user_id: number }>>(
        "/auth/register",
        { email, password, full_name: fullName }
      );
      localStorage.setItem("auth_token", res.data.token);
      setState({ user: null, isAuthenticated: true, loading: false });
      return res.data;
    },
    []
  );

  const logout = useCallback(() => {
    localStorage.removeItem("auth_token");
    setState({ user: null, isAuthenticated: false, loading: false });
  }, []);

  return { ...state, login, register, logout };
}
