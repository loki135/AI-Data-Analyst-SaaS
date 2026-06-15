/**
 * Shared client-side validation helpers.
 *
 * Mirrors backend validation rules so the UI can provide
 * instant feedback without a round-trip, while the backend
 * remains the authoritative validator.
 */

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateEmail(email: string): ValidationResult {
  const errors: string[] = [];
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!pattern.test(email.trim())) {
    errors.push("Must be a valid email address");
  }
  return { valid: errors.length === 0, errors };
}

export function validatePassword(password: string): ValidationResult {
  const errors: string[] = [];
  if (password.length < 8) errors.push("Must be at least 8 characters");
  if (!/[A-Z]/.test(password)) errors.push("Must contain an uppercase letter");
  if (!/[a-z]/.test(password)) errors.push("Must contain a lowercase letter");
  if (!/\d/.test(password)) errors.push("Must contain a digit");
  return { valid: errors.length === 0, errors };
}

export function validateRequired(value: string, fieldName: string): ValidationResult {
  const trimmed = value.trim();
  if (!trimmed) {
    return { valid: false, errors: [`${fieldName} is required`] };
  }
  return { valid: true, errors: [] };
}

export function validateFileExtension(
  filename: string,
  allowed: string[] = [".csv", ".xlsx", ".xls", ".json", ".parquet"]
): ValidationResult {
  const ext = filename.slice(filename.lastIndexOf(".")).toLowerCase();
  if (!allowed.includes(ext)) {
    return { valid: false, errors: [`File type ${ext} is not supported. Use: ${allowed.join(", ")}`] };
  }
  return { valid: true, errors: [] };
}
