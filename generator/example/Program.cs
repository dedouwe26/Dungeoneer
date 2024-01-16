class Program
{
    public static void Main ()
    {
        Dungeoneer.Map map = new Dungeoneer.Map(new Dungeoneer.GeneratorConfig(), new Random());
        Console.WriteLine(map.ToMap());
    }
}