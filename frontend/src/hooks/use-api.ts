/**
 * Shared React hook for API calls with loading/error state.
 *
 * Eliminates duplicated loading/error/data state management
 * that would otherwise appear in every component that fetches data.
 */

"use client";

import { useCallback, useState } from "react";

interface UseApiState<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}

interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: unknown[]) => Promise<T | null>;
  reset: () => void;
}

export function useApi<T>(
  apiCall: (...args: unknown[]) => Promise<T>
): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    error: null,
    loading: false,
  });

  const execute = useCallback(
    async (...args: unknown[]): Promise<T | null> => {
      setState({ data: null, error: null, loading: true });
      try {
        const data = await apiCall(...args);
        setState({ data, error: null, loading: false });
        return data;
      } catch (err) {
        const message = err instanceof Error ? err.message : "An error occurred";
        setState({ data: null, error: message, loading: false });
        return null;
      }
    },
    [apiCall]
  );

  const reset = useCallback(() => {
    setState({ data: null, error: null, loading: false });
  }, []);

  return { ...state, execute, reset };
}
