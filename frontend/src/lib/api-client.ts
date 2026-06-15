/**
 * Centralized API client.
 *
 * Every component that makes API calls uses this single client,
 * which handles:
 * - Base URL configuration
 * - Auth token injection
 * - Consistent error parsing
 * - Response type narrowing
 *
 * This eliminates duplicated fetch/axios wrappers across pages.
 */

import type { ApiError, ApiResponse, PaginatedResponse } from "@/types/api";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class ApiClientError extends Error {
  status: number;
  detail: ApiError["error"];

  constructor(status: number, detail: ApiError["error"]) {
    super(detail.message);
    this.status = status;
    this.detail = detail;
  }
}

function getAuthHeaders(): HeadersInit {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("auth_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(
  method: string,
  path: string,
  options: { body?: unknown; params?: Record<string, string> } = {}
): Promise<T> {
  const url = new URL(`${BASE_URL}${path}`);
  if (options.params) {
    Object.entries(options.params).forEach(([k, v]) => url.searchParams.set(k, v));
  }

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...getAuthHeaders(),
  };

  const res = await fetch(url.toString(), {
    method,
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!res.ok) {
    const errorBody = (await res.json()) as ApiError;
    throw new ApiClientError(res.status, errorBody.error);
  }

  return res.json() as Promise<T>;
}

/**
 * Upload a file via multipart/form-data.
 */
async function upload<T>(path: string, file: File, fieldName = "file"): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const formData = new FormData();
  formData.append(fieldName, file);

  const res = await fetch(url, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });

  if (!res.ok) {
    const errorBody = (await res.json()) as ApiError;
    throw new ApiClientError(res.status, errorBody.error);
  }

  return res.json() as Promise<T>;
}

export const apiClient = {
  get: <T>(path: string, params?: Record<string, string>) =>
    request<T>("GET", path, { params }),

  post: <T>(path: string, body?: unknown) =>
    request<T>("POST", path, { body }),

  put: <T>(path: string, body?: unknown) =>
    request<T>("PUT", path, { body }),

  delete: <T>(path: string) => request<T>("DELETE", path),

  upload: <T>(path: string, file: File, fieldName?: string) =>
    upload<T>(path, file, fieldName),
};

export { ApiClientError };
export type { ApiResponse, PaginatedResponse };
