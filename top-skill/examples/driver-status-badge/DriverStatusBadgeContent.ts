import {
  DriverStatusBadgeControllerAccess,
  DriverStatusTone,
} from "./DriverStatusBadgeControllerAccess";

export type DriverStatusBadgeOutput = {
  readonly kind: "driver-status-badge";
  readonly text: string;
  readonly tone: DriverStatusTone;
  readonly verifierStatus: string;
  readonly deliveryStatus: string;
};

export type DriverStatusBadgeContentProps = {
  readonly owner: DriverStatusBadgeControllerAccess;
};

export function DriverStatusBadgeContent(
  props: DriverStatusBadgeContentProps,
): DriverStatusBadgeOutput {
  const owner = props.owner;

  return {
    kind: "driver-status-badge",
    text: owner.getBadgeText(),
    tone: owner.getTone(),
    verifierStatus: owner.getVerifierStatusText(),
    deliveryStatus: owner.getDeliveryStatusText(),
  };
}
