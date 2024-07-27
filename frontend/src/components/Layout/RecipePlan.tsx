"use client";
import { useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import breakfast from "../../../../public/svg/breakfast.svg";
import dinner from "../../../../public/svg/dinner.svg";
import dessert from "../../../../public/svg/dessert.svg";
import salad from "../../../../public/svg/salad.svg";
import lunch from "../../../../public/svg/lunch.png";
import styles from "./Recipe.module.css";
export default function RegisterPlan() {
  const [selectedCategory, setSelectedCategory] = useState("");

  function handleCategory(category: string) {
    setSelectedCategory(category);
  }
  return (
    <main className={styles["recipe__plan"]}>
      <Button
        className={`${selectedCategory === "breakfast" ? styles.active : ""}`}
        onClick={() => handleCategory("breakfast")}
      >
        <Image src={breakfast} width={20} height={30} alt="" />
        Breakfast
      </Button>
      <Button
        className={`${selectedCategory === "lunch" ? styles.active : ""}`}
        onClick={() => handleCategory("lunch")}
      >
        <Image src={lunch} width={20} height={30} alt="" />
        Lunch
      </Button>
      <Button
        className={`${selectedCategory === "dinner" ? styles.active : ""}`}
        onClick={() => handleCategory("dinner")}
      >
        <Image src={dinner} width={20} height={30} alt="" />
        Dinner
      </Button>
      <Button
        className={`${selectedCategory === "dessert" ? styles.active : ""}`}
        onClick={() => handleCategory("dessert")}
      >
        <Image src={dessert} width={20} height={30} alt="" />
        Dessert
      </Button>
      <Button
        className={`${selectedCategory === "salads" ? styles.active : ""}`}
        onClick={() => handleCategory("salads")}
      >
        <Image src={salad} width={20} height={30} alt="" />
        Salads
      </Button>
    </main>
  );
}
