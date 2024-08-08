import MealTable from "./MealTable";
import Image from "next/image";
import deletez from "../../../../public/svg/delete.svg";
import edit from "../../../../public/svg/edit.svg";
import styles from "./MealPlan.module.css";
export default function MealPlan() {
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
