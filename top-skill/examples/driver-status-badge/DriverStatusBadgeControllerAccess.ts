export type DriverStatusTone = "success" | "warning" | "neutral";

export interface DriverStatusBadgeControllerAccess {
  getBadgeText(): string;
  getTone(): DriverStatusTone;
  getVerifierStatusText(): string;
  getDeliveryStatusText(): string;
}
