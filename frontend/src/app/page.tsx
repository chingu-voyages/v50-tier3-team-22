import { lazy } from "react";
import MealPlan from "@/components/Layout/mealPlan/MealPlan";

const SignInPreview = lazy(() => import("../components/Layout/auth/LoginComp"));
export default function Home() {
  return (
    <main>
      {/* <SignInPreview /> */}
      <MealPlan />
    </main>
  );
}
