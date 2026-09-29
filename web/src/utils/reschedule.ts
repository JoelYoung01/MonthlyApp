import type { AppDefinitionDashboard } from "@/types";

export type MonthKey = `${number}-${string}`;

export function parseAppDate(value: string) {
  const datePart = value.slice(0, 10);
  const [year, month, day] = datePart.split("-").map(Number);
  return new Date(year, month - 1, day);
}

export function toMonthKey(date: Date): MonthKey {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  return `${year}-${month}`;
}

export function monthKeyFromParts(year: number, monthIndex: number): MonthKey {
  const normalized = new Date(year, monthIndex, 1);
  return toMonthKey(normalized);
}

export function monthKeyToIndex(key: string) {
  const [year, month] = key.split("-").map(Number);
  return year * 12 + (month - 1);
}

export function indexToMonthKey(index: number): MonthKey {
  const year = Math.floor(index / 12);
  const month = (index % 12) + 1;
  return `${year}-${String(month).padStart(2, "0")}`;
}

export function appStartMonthKey(app: AppDefinitionDashboard): MonthKey {
  return toMonthKey(parseAppDate(app.start_date));
}

export function appsForMonthKey(apps: AppDefinitionDashboard[], key: string) {
  const [year, month] = key.split("-").map(Number);
  const monthStart = new Date(year, month - 1, 1).getTime();
  const monthEnd = new Date(year, month, 0).getTime();
  return apps.filter((app) => {
    const start = parseAppDate(app.start_date).getTime();
    const due = parseAppDate(app.due_date).getTime();
    return start <= monthEnd && due >= monthStart;
  });
}

export function shiftDateByMonths(value: string, deltaMonths: number) {
  const date = parseAppDate(value);
  const day = date.getDate();
  const shifted = new Date(date.getFullYear(), date.getMonth() + deltaMonths, 1);
  const lastDay = new Date(shifted.getFullYear(), shifted.getMonth() + 1, 0).getDate();
  shifted.setDate(Math.min(day, lastDay));
  return toApiDate(shifted);
}

export function toApiDate(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  // Match existing create/update convention used by the app
  return new Date(`${year}-${month}-${day}T00:00:00`).toISOString().replace("Z", "");
}

export function shiftAppByMonths(
  app: AppDefinitionDashboard,
  deltaMonths: number
): AppDefinitionDashboard {
  return {
    ...app,
    start_date: shiftDateByMonths(app.start_date, deltaMonths),
    due_date: shiftDateByMonths(app.due_date, deltaMonths)
  };
}

function occupancyByStartMonth(apps: AppDefinitionDashboard[]) {
  const map = new Map<number, AppDefinitionDashboard>();
  for (const app of apps) {
    map.set(monthKeyToIndex(appStartMonthKey(app)), app);
  }
  return map;
}

/**
 * Move an app so its start month becomes `targetMonthKey`.
 * If that month is occupied, shift only the consecutive occupied block from the
 * target forward until the next empty month; apps after that gap stay put.
 */
export function previewMoveAppToMonth(
  apps: AppDefinitionDashboard[],
  appId: number,
  targetMonthKey: string
): AppDefinitionDashboard[] {
  const dragged = apps.find((app) => app.id === appId);
  if (!dragged) return apps.map((app) => ({ ...app }));

  const currentIndex = monthKeyToIndex(appStartMonthKey(dragged));
  const targetIndex = monthKeyToIndex(targetMonthKey);
  if (currentIndex === targetIndex) {
    return apps.map((app) => ({ ...app }));
  }

  const others = apps.filter((app) => app.id !== appId);
  const occupancy = occupancyByStartMonth(others);

  let nextOthers = others.map((app) => ({ ...app }));
  if (occupancy.has(targetIndex)) {
    let gapIndex = targetIndex;
    while (occupancy.has(gapIndex)) {
      gapIndex += 1;
    }

    // Shift only the filled run [target, gap) — leave everything after the opening alone
    nextOthers = nextOthers.map((app) => {
      const idx = monthKeyToIndex(appStartMonthKey(app));
      if (idx >= targetIndex && idx < gapIndex) {
        return shiftAppByMonths(app, 1);
      }
      return app;
    });
  }

  const moved = shiftAppByMonths(dragged, targetIndex - currentIndex);
  return [...nextOthers, moved];
}

export function previewShiftAppByMonths(
  apps: AppDefinitionDashboard[],
  appId: number,
  deltaMonths: number
): AppDefinitionDashboard[] {
  const dragged = apps.find((app) => app.id === appId);
  if (!dragged || deltaMonths === 0) return apps.map((app) => ({ ...app }));

  const targetIndex = monthKeyToIndex(appStartMonthKey(dragged)) + deltaMonths;
  return previewMoveAppToMonth(apps, appId, indexToMonthKey(targetIndex));
}

export function appsDifferingDates(
  original: AppDefinitionDashboard[],
  next: AppDefinitionDashboard[]
) {
  const byId = new Map(original.map((app) => [app.id, app]));
  return next.filter((app) => {
    const prev = byId.get(app.id);
    if (!prev) return true;
    return prev.start_date !== app.start_date || prev.due_date !== app.due_date;
  });
}
