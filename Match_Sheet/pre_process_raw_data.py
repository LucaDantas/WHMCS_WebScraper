import csv

# select the location of the data files accordingly
csv_domains = 'raw/domains.csv'
csv_subdomains = 'raw/subdomains.csv'
csv_websites = 'raw/websites.csv'
csv_clients = 'raw/clients.csv'

csv_out_domains = 'data/domains.csv'
csv_out_subdomains = 'data/subdomains.csv'
csv_out_websites = 'data/websites.csv'
csv_out_clients = 'data/clients.csv'

def main():
    # read the csv files and put them through the csv library
    with open(csv_domains, 'r') as domf, open(csv_subdomains, 'r') as subdf, open(csv_websites, 'r') as webf, open(csv_clients, 'r') as clif,\
            open(csv_out_domains, 'w') as out_domf, open(csv_out_subdomains, 'w') as out_subdf, open(csv_out_websites, 'w') as out_webf, open(csv_out_clients, 'w') as out_clif:
        domains = csv.reader(domf)
        subdomains = csv.reader(subdf)
        websites = csv.reader(webf)
        clients = csv.reader(clif)

        out_domains = csv.writer(out_domf)
        out_subdomains = csv.writer(out_subdf)
        out_websites = csv.writer(out_webf)
        out_clients = csv.writer(out_clif)

        first = True
        for row in subdomains:
            if first:
                first = False
                continue
            out_subdomains.writerow((row[0][:-1], row[1])) # for some reason it scrapes with an extra space at the end

        first = True
        for row in domains:
            if first:
                first = False
                continue
            out_domains.writerow((row[0], row[3]))

        first = True
        for row in websites:
            if first:
                first = False
                continue
            out_websites.writerow((row[0], row[3]))

        for row in clients:
            out_clients.writerow((row[1] + ' ' + row[2], row[3], row[5]))

if __name__ == '__main__':
    main()
