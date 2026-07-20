def export_txt(results):

    with open("results.txt", "w", encoding="utf-8") as file:

        file.write("PORT     STATUS   SERVICE     BANNER\n")
        file.write("-" * 50 + "\n")

        for puerto, service, banner in results:
            file.write(f"{puerto:<8} OPEN     {service:<10} {banner}\n")