import AddRecipeForm from "@/components/Layout/newRecipe/AddRecipeForm";
import { fastApi } from "@/lib/axios";

export default async function AddRecipe() {
  const { data } = await fastApi.get("/recipe/options");

  if (!data) {
    return <div>Something went wrong</div>;
  }

  return <AddRecipeForm categories={data.category} levels={data.level} />;
}
