import styles from "./MealPlan.module.css";

interface Props {
  day: string;
  breakfast: string;
  snack: string;
  lunch: string;
  dinner: string;
}
export default function MealTable({
  day,
  breakfast,
  lunch,
  snack,
  dinner,
}: Props) {
  return (
    <main className={styles.table}>
      <table>
        <thead>
          <tr>
            <th scope="col" className={styles["empty__cell"]}></th>
            <th scope="col">Breakfast</th>
            <th scope="col">Lunch</th>
            <th scope="col">Snack</th>
            <th scope="col">Dinner</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row" className={styles.days}>
              {day}
            </th>
            <td>{breakfast}</td>
            <td>{lunch}</td>
            <td>{snack}</td>
            <td>{dinner}</td>
          </tr>
        </tbody>
      </table>
    </main>
  );
}
