
import RecipeDetails from "@/components/Layout/RecipeDetails";

import LoginComp from "@/components/Layout/auth/LoginComp";


export default function Home() {
  return (
    <main>
      <p className="text-primary">Recepies Shopping List</p>
      <RecipeDetails />
      {/* <p>Recepies Shopping List</p> */}
      <LoginComp />
    </main>
  );
}
