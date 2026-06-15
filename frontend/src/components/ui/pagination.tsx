/**
 * Shared pagination component.
 *
 * Used by all list views (datasets, analyses) to avoid
 * duplicated pagination UI and logic.
 */

import type { PaginationMeta } from "@/types/api";

interface PaginationProps {
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
}

export function Pagination({ pagination, onPageChange }: PaginationProps) {
  const { page, total_pages } = pagination;

  if (total_pages <= 1) return null;

  return (
    <nav className="flex items-center justify-center gap-2 py-4" aria-label="Pagination">
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        className="rounded border px-3 py-1 text-sm disabled:opacity-50"
      >
        Previous
      </button>
      <span className="text-sm text-gray-600">
        Page {page} of {total_pages}
      </span>
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page >= total_pages}
        className="rounded border px-3 py-1 text-sm disabled:opacity-50"
      >
        Next
      </button>
    </nav>
  );
}
