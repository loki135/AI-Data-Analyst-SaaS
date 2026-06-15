/**
 * Shared error display component.
 *
 * Used across all pages to display API or validation errors
 * with a consistent UI instead of ad-hoc inline messages.
 */

interface ErrorMessageProps {
  message: string | null;
  className?: string;
}

export function ErrorMessage({ message, className = "" }: ErrorMessageProps) {
  if (!message) return null;
  return (
    <div
      role="alert"
      className={`rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700 ${className}`}
    >
      {message}
    </div>
  );
}
