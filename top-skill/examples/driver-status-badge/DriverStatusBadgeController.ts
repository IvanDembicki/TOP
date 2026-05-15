import {
  DriverStatusBadgeControllerAccess,
  DriverStatusTone,
} from "./DriverStatusBadgeControllerAccess";

export class DriverStatusBadgeController
  implements DriverStatusBadgeControllerAccess {
  public getContentAccess(): DriverStatusBadgeControllerAccess {
    return this;
  }

  public getBadgeText(): string {
    return "RUN_VALID certified";
  }

  public getTone(): DriverStatusTone {
    return "success";
  }

  public getVerifierStatusText(): string {
    return "Verifier: RUN_VALID certified";
  }

  public getDeliveryStatusText(): string {
    return "Delivery: complete";
  }
}
