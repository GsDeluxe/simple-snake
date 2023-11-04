using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Deluxe
{
    class Snake
    {
        public static void Main()
        {
            Snake snake = new Snake();
            snake.snake_game();
        }
        public void snake_game()
        {
            int TERMINAL_COLUMNS = Console.WindowWidth;
            int TERMINAL_LINES = Console.WindowHeight;
            int INC = 0;
            int SNAKE_LENGTH = 4;

            Random random = new Random();

            List<int> food_cords = new List<int> { random.Next(1, TERMINAL_COLUMNS), random.Next(1, TERMINAL_LINES) };

            string direction = "UP";
            List<List<int>> snake_cord = new List<List<int>> { new List<int> { TERMINAL_COLUMNS / 2, TERMINAL_LINES / 2 } };


            while (true)
            {
                Console.Clear();

                Console.SetCursorPosition(food_cords[0], food_cords[1]);
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("$");
                Console.ResetColor();

                if (Console.KeyAvailable)
                {
                    var key = Console.ReadKey(true).Key;
                    if ((key == ConsoleKey.UpArrow || key == ConsoleKey.W) && direction != "DOWN")
                    {
                        direction = "UP";
                    }
                    else if ((key == ConsoleKey.DownArrow || key == ConsoleKey.S) && direction != "UP")
                    {
                        direction = "DOWN";
                    }
                    else if ((key == ConsoleKey.LeftArrow || key == ConsoleKey.A) && direction != "RIGHT")
                    {
                        direction = "LEFT";
                    }
                    else if ((key == ConsoleKey.RightArrow || key == ConsoleKey.D) && direction != "LEFT")
                    {
                        direction = "RIGHT";
                    }
                    else if (key == ConsoleKey.Escape)
                    {
                        goto EndWhile;
                    }

                }


                if (direction == "UP")
                {
                    snake_cord.Add(new List<int> { snake_cord[INC][0], snake_cord[INC][1] - 1 });
                }
                else if (direction == "DOWN")
                {
                    snake_cord.Add(new List<int> { snake_cord[INC][0], snake_cord[INC][1] + 1 });
                }
                else if (direction == "LEFT")
                {
                    snake_cord.Add(new List<int> { snake_cord[INC][0] - 1, snake_cord[INC][1] });
                }
                else if (direction == "RIGHT")
                {
                    snake_cord.Add(new List<int> { snake_cord[INC][0] + 1, snake_cord[INC][1] });
                }

                if (snake_cord.Count() > SNAKE_LENGTH)
                {
                    snake_cord.RemoveAt(0);
                    INC = INC - 1;
                }

                INC = INC + 1;


                foreach (var cord in snake_cord)
                {

                    if (cord[0] == 0 || cord[1] == 0 || cord[0] == TERMINAL_COLUMNS - 1 || cord[1] == TERMINAL_LINES - 1)
                    {
                        goto EndWhile;
                    }

                    if ((cord[0] == food_cords[0]) && (cord[1] == food_cords[1]))
                    {
                        SNAKE_LENGTH++;
                        food_cords[0] = random.Next(1, TERMINAL_COLUMNS);
                        food_cords[1] = random.Next(1, TERMINAL_LINES);

                    }


                    Console.SetCursorPosition(cord[0], cord[1]);
                    Console.WriteLine("*");
                }
                Thread.Sleep(10);
            }
        EndWhile:
            Console.Clear();
            Console.WriteLine("Died");
            Console.WriteLine("\n\n");
            Console.ReadKey();

        }
    }
}
