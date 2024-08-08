import Image from "next/image";
import Link from "next/link";
import { PlusIcon } from "@radix-ui/react-icons";
import { Button } from "@/components/ui/button";
import RegisterPlan from "./RecipePlan";
import recipe from "../../../../public/pictures/recipe.png";
import bookmark from "../../../../public/svg/bookmark.svg";
import styles from "./Recipe.module.css";
export default function Recipes() {
  return (
    <main className={styles.container}>
      <div className={styles.header}>
        <h2>Recipes</h2>
        <Button>
          <PlusIcon className={styles["plus__icon"]} />
          Add recipes
        </Button>
      </div>
      <div>
        <RegisterPlan />
      </div>
      <section className={styles["recipe__items"]}>
        <div className={styles["recipe__card"]}>
          <div>
            <Image src={recipe} width={600} height={500} alt="" />
          </div>
          <div className={styles["recipe__title"]}>
            <Link href={""}>
              <h3>Lemon Chicken</h3>
            </Link>
            <button>
              <Image src={bookmark} width={20} height={10} alt="" />
            </button>
          </div>
          <div className={styles["meal__deets"]}>
            <span>Italian</span>
            <span>Easy</span>
            <span>30 min</span>
          </div>
        </div>
        <div className={styles["recipe__card"]}>
          <div>
            <Image src={recipe} width={600} height={500} alt="" />
          </div>
          <div className={styles["recipe__title"]}>
            <Link href={""}>
              <h3>Lemon Chicken</h3>
            </Link>
            <button>
              <Image src={bookmark} width={20} height={10} alt="" />
            </button>
          </div>
          <div className={styles["meal__deets"]}>
            <span>Italian</span>
            <span>Easy</span>
            <span>30 min</span>
          </div>
        </div>
        <div className={styles["recipe__card"]}>
          <div>
            <Image src={recipe} width={600} height={500} alt="" />
          </div>
          <div className={styles["recipe__title"]}>
            <Link href={""}>
              <h3>Lemon Chicken</h3>
            </Link>
            <button>
              <Image src={bookmark} width={20} height={10} alt="" />
            </button>
          </div>
          <div className={styles["meal__deets"]}>
            <span>Italian</span>
            <span>Easy</span>
            <span>30 min</span>
          </div>
        </div>
        <div className={styles["recipe__card"]}>
          <div>
            <Image src={recipe} width={600} height={500} alt="" />
          </div>
          <div className={styles["recipe__title"]}>
            <Link href={""}>
              <h3>Lemon Chicken</h3>
            </Link>
            <button>
              <Image src={bookmark} width={20} height={10} alt="" />
            </button>
          </div>
          <div className={styles["meal__deets"]}>
            <span>Italian</span>
            <span>Easy</span>
            <span>30 min</span>
          </div>
        </div>
      </section>
    </main>
  );
}
