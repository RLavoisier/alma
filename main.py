from factory import Factory
from game_settings import (
    TARGET_NB_ROBOTS,
    DEFAULT_ROBOT_MONEY_COST,
    DEFAULT_ROBOT_FOO_COST,
)
from jobs import MiningFoo, MiningBar, ChangeJob, AssemblingFooBar, SellFooBar
from stock import Stock
from work_session import WorkSession

if __name__ == "__main__":
    stock = Stock()
    factory = Factory()

    factory.create_worker()
    bar_job = MiningBar()
    factory.create_worker(bar_job)

    def spoiler():
        if stock.foo < DEFAULT_ROBOT_FOO_COST or stock.money < DEFAULT_ROBOT_MONEY_COST:
            return "(Spoiler alert : You don't have enough ressources)"

    menu_entries = {
        1: "Show your current robots",
        2: f"Hire a new robot (Cost {DEFAULT_ROBOT_MONEY_COST}€ and {DEFAULT_ROBOT_FOO_COST} foos) {spoiler()}",
        3: "Change a robot's job",
        4: "Show you current ressources",
        5: "Show you current Foobar list",
        6: "Start a new work session",
    }

    def show_menu():
        for entry, prompt in menu_entries.items():
            print(f"{entry} - {prompt}")

    def show_robots_list():
        print("Your Worker list :")
        for w in factory.workers:
            print(f"{w.id} - {w.name} - Working on {w.job.name}")

    available_jobs = {1: MiningFoo, 2: MiningBar, 3: AssemblingFooBar, 4: SellFooBar}

    print("-" * 65)
    print("----------- [[-_-]] Welcome in FooBar Tycoon ! [[-_-]] ----------")
    print("-" * 65)
    print(stock)

    while len(factory.workers) < TARGET_NB_ROBOTS:
        print("-" * 65)
        print("Prepare your next work day for your hard working robots:")
        show_menu()

        try:
            choice = int(input("Your choice:"))
            if choice not in menu_entries.keys():
                raise ValueError
        except ValueError:
            print("Please choose an existing menu value,")
            continue

        print("-" * 65)

        if choice == 1:
            show_robots_list()
        if choice == 2:
            if (
                stock.foo < DEFAULT_ROBOT_FOO_COST
                or stock.money < DEFAULT_ROBOT_MONEY_COST
            ):
                print("Well...Guess what...You don't have enough ressources !")
            else:
                worker = factory.create_worker()
                stock.foo -= 6
                stock.money -= 3
                print(f"Congratulations ! {worker.name} joins the team !")
        elif choice == 3:
            show_robots_list()
            print("-" * 65)
            try:
                robot_id = int(
                    input("Enter the id of the robot that should change its job:")
                )
                if robot_id not in [r.id for r in factory.workers]:
                    raise ValueError
            except ValueError:
                print(
                    "Sorry, this robot doesn't exist (or has been bent, crushed or dumped away)."
                )
                continue

            robot = next(iter([r for r in factory.workers if r.id == robot_id]))

            try:
                print("-" * 65)
                print(f"Ahhh this good old {robot.name} !")
                job_list = [f"{k} - {v.name}" for k, v in available_jobs.items()]
                new_job_class_id = int(
                    input(f"What should be its new job ? " f"({job_list}):")
                )
                if new_job_class_id not in available_jobs.keys():
                    raise ValueError
            except ValueError:
                print("This job is not compatible with our robots...")
                continue
            new_job = available_jobs[new_job_class_id]()
            robot.job = ChangeJob(new_job)
            print("-" * 65)
            print(
                "Done ! Our best engineers will work hard to reprogram {robot.name}"
                "during the next work session"
            )
        elif choice == 4:
            print("Your current balance is:")
            print(stock)
        elif choice == 5:
            print("Your Foobar product list contains:")
            for foobar in stock.foobar:
                print(foobar)
            if not stock.foobar():
                print("Sadly...Nothing...")
        elif choice == 6:
            print("Everyone is ready to work !")
            try:
                work_session_duration = int(
                    input("How long in second should be this work session ?")
                )
            except ValueError:
                print("Uhhhhh...We'll just habe a bank holliday then...")
                continue

            work_session = WorkSession(factory, work_session_duration)
            print("The work session is starting ! LET'S GO !")
            work_session.start()
    else:
        print("CONGRATULATIONS ! YOU WON !")
        print("Those robots are going on holliday now")
