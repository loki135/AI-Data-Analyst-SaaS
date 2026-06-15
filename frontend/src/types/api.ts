/**
 * Shared API response types.
 *
 * These mirror the backend response envelope so every component
 * that consumes API data uses a single, consistent shape.
 */

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: Record<string, unknown>;
}

export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: PaginationMeta;
}

export interface ApiError {
  error: {
    message: string;
    status_code: number;
    [key: string]: unknown;
  };
}

export interface Dataset {
  id: number;
  name: string;
  description?: string;
  row_count: number;
  column_count: number;
  created_at: string;
}

export interface Analysis {
  id: number;
  title: string;
  query: string;
  result_summary: string;
  status: "pending" | "completed" | "failed";
  dataset_id: number;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
}
