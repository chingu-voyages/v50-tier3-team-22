"use client";
import { useEffect } from "react";
import MealTable from "./MealTable";
import Image from "next/image";
import deletez from "../../../../public/svg/delete.svg";
import edit from "../../../../public/svg/edit.svg";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fastApi } from "@/lib/axios";
import styles from "./MealPlan.module.css";

interface MealPlanDataProps {
  day: string;
  breakfast: string;
  lunch: string;
  snack: string;
  dinner: string;
}
export default function MealPlan() {
  const queryClient = useQueryClient();

  // Fetch data using useQuery
  const { isPending, error, data } = useQuery({
    queryKey: ["fetchMealPlan"],
    queryFn: async () => {
      const response = await fastApi.get("/endpoint");
      return response.data;
    },
  });

  useEffect(() => {
    const handlePageload = () => {
      // Refetch the data manually on window reload
      queryClient.invalidateQueries({ queryKey: ["fetchMealPlan"] });
    };

    // Add event listener for window reload
    window.addEventListener("load", handlePageload);

    // Cleanup event listener on component unmount
    return () => {
      window.removeEventListener("load", handlePageload);
    };
  }, [queryClient]);

  return (
    <main className={styles.container}>
      <h2>Meal Plan</h2>
      <div>
        <div className={styles.buttons}>
          <button>
            <Image src={edit} width={10} height={10} alt="" />
            Edit
          </button>
          <button>
            <Image src={deletez} width={10} height={10} alt="" />
            Delete
          </button>
        </div>
        <MealTable
          day={"Monday"}
          breakfast={`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor`}
          lunch={`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor`}
          snack={`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor`}
          dinner={`Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor`}
        />
      </div>
    </main>
  );
}
