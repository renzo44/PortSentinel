import csv
import json

def export_txt(results):

    with open("results.txt", "w", encoding="utf-8") as file:

        file.write("PORT     STATUS   SERVICE     BANNER\n")
        file.write("-" * 50 + "\n")

        for puerto, service, banner in results:
            file.write(f"{puerto:<8} OPEN     {service:<10} {banner}\n")
            
def export_csv(results):

    with open("results.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["PORT", "STATUS", "SERVICE", "BANNER"])

        for puerto, service, banner in results:
            writer.writerow([puerto, "OPEN", service, banner])
            

def export_json(results):

    data = []

    for puerto, service, banner in results:

        data.append({
            "port": puerto,
            "status": "OPEN",
            "service": service,
            "banner": banner
        })

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)