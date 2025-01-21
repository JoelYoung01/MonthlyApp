export function formatDate(dateString?: string, includeTime = false): string {
  if (!dateString) return "";

  const date = new Date(dateString);

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
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
