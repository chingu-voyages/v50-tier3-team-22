import AddRecipeForm from "@/components/Layout/newRecipe/AddRecipeForm";
import { fastApi } from "@/lib/axios";

export default async function AddRecipe() {
  const { data } = await fastApi.get("/recipe/options");

  return <AddRecipeForm categories={data.category} levels={data.level} />;
}
