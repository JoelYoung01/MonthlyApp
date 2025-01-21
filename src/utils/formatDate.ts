export function formatDate(
  dateString?: string,
  excludeCurrentYear = false,
  includeTime = false
): string {
  if (!dateString) return "";

  const date = new Date(dateString);
  const today = new Date();

  const sameYear = date.getFullYear() === today.getFullYear();

  const options: Intl.DateTimeFormatOptions = {
    year: sameYear && excludeCurrentYear ? undefined : "numeric",
    month: "short",
    day: "numeric"
  };

  if (includeTime) {
    options.hour = "2-digit";
    options.minute = "2-digit";
    options.second = "2-digit";
  }

  return (
    date.toLocaleDateString(undefined, options) +
    (includeTime ? ` ${date.toLocaleTimeString(undefined, options)}` : "")
  );
}
