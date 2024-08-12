"use client";
import AddRecipeForm from "@/components/Layout/newRecipe/AddRecipeForm";
import { fastApi } from "@/lib/axios";
import { useState } from "react";

export default function AddRecipe() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<boolean>(false);

  async function sendOptions() {
    try {
      const response = await fastApi.get("/recipe/options");
      if (response?.status === 200) {
        setData(response.data);
      } else {
        console.log({ response });

        setError(true);
      }
    } catch (error) {
      console.log({ error });
      setError(true);
    }
  }

  if (error) {
    return <div>Something went wrong</div>;
  }

  if (!data) {
    return <div>Loading...</div>;
  }

  return <AddRecipeForm categories={data.category} levels={data.level} />;
}
