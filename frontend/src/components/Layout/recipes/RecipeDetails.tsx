import Image from "next/image";
import recipe from "../../../../public/pictures/recipe.png";
import deletez from "../../../../public/svg/delete.svg";
import edit from "../../../../public/svg/edit.svg";
import styles from "./RecipeDetails.module.css";
export default function RecipeDetails() {
  return (
    <main className={styles.container}>
      <div className={styles.info}>
        <h2>Lemon Chicken </h2>
        <p className={styles.plan}>Lunch</p>
        <div className={styles["meal__deets"]}>
          <span>Italian</span>
          <span>Easy</span>
          <span>30 min</span>
        </div>
        <Image src={recipe} width={480} height={280} alt="" />
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
        <div>
          <p className={styles["recipe__note"]}>
            Lorem Ipsum is simply dummy text of the printing and typesetting
            industry. Lorem Ipsum has been the industry's standard dummy text
            ever since the 1500s, when an unknown printer took a galley of type
            and scrambled it to make a type specimen book. It has survived not
            only five centuries, but also the leap into electronic typesetting,
            remaining essentially unchanged. It was popularised in the 1960s
            with the release of Letraset sheets containing Lorem Ipsum passages,
            and more recently with desktop publishing software like Aldus
            PageMaker including versions of Lorem Ipsum.
          </p>
        </div>
      </div>
      <div className={styles["check__boxes"]}>
        <h2>Ingredients</h2>
        <ul>
          <li>
            <input type="checkbox" className={styles.checkbox} />
            lorem ipsum
          </li>
          <li>
            <input type="checkbox" className={styles.checkbox} /> lorem ipsum
          </li>
          <li>
            <input type="checkbox" className={styles.checkbox} /> lorem ipsum
          </li>
          <li>
            <input type="checkbox" className={styles.checkbox} /> lorem ipsum
          </li>
        </ul>
      </div>
    </main>
  );
}
