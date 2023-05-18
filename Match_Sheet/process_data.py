import csv

# select the location of the data files accordingly
csv_domains = 'data/domains.csv'
csv_subdomains = 'data/subdomains.csv'
csv_websites = 'data/websites.csv'
csv_clients = 'data/clients.csv'
csv_matched = 'match_sheet.csv'
csv_not_matched = 'not_matched.csv'

class Domain:
    def __init__(self, domain_name):
        self.name = domain_name
        self.subdomains = []
        self.websites = []

    def add_website(self, website_name):
        self.websites.append(website_name)

    def add_subdomain(self, subdomain_name):
        self.subdomains.append(subdomain_name)

    # Removes the subdomains which are already counted in the websites
    def clean_subdomains(self):
        aux = []
        for subdomain in self.subdomains:
            if (subdomain + '/') not in self.websites:
                aux.append(subdomain)
        self.subdomains = aux

class Client:
    def __init__(self, _name, _email, _role):
        self.name = _name
        self.email = _email
        self.role = _role
        self.domains = [Domain('[Other]')] # Already initialize it with the "Other" domain, put it on the last place at the end
    
    def add_domain(self, domain):
        self.domains.append(domain)

def match_data(domains, subdomains, websites, clients):
    clients_table = {} # create it as a dictionary of the emails because it's easier to access later
    domains_owner = {} # dictionary between domain name and its owner, used to match subdomains
    domains_not_matched = [] # list of pairs (admin email, domain)
    websites_not_matched = [] # list of pairs (admin email, website)

    for row in clients:
        # change the indexes of row[i] to accomodate for the given data, put them correctly for name, email and role
        name = row[0]
        email = row[1]
        role = row[2]

        # add this client to the table, make sure all the emails of the clients are unique
        clients_table[email] = Client(name, email, role)

    for row in domains:
        domain_name = row[0]
        domains_owner[domain_name] = row[1]
        owners = row[1].split(', ') # a domain might have multiple owners, which are separated by ", "
        for owner in owners:
            if owner in clients_table: # if the owner has a WHMCS account I match the domain to its account
                if clients_table[owner]:
                    clients_table[owner].add_domain(Domain(domain_name))
            else: # otherwise I add it to the list of unmatched domains
                domains_not_matched.append((owner, domain_name))

    for row in subdomains:
        domain_name = row[0]
        subdomain_name = row[1]

        if subdomain_name == "No subdomains": # The way I scraped the data it produced No subdomains if the domain didn't have any subdomains, which I want to ignore now
            continue

        for owner in domains_owner[domain_name].split(', '):
            if owner not in clients_table: # I'm ignoring the ones that don't have an account in WHMCS
                continue
            # find the domain the subdomain belongs to and add it
            for domain in clients_table[owner].domains:
                if domain.name == domain_name:
                    domain.add_subdomain(subdomain_name)

    for row in websites:
        website_name = row[0]
        admin_email = row[1]
        if(admin_email not in clients_table): # if the admin of this website doesn't have an account I add it to the list of unmatched websites
            websites_not_matched.append((admin_email, website_name))
        else: # otherwise I match it to its domain
            cnt = 0
            for domain in clients_table[admin_email].domains:
                if domain.name in website_name:
                    domain.add_website(website_name)
                    cnt += 1
            assert (cnt <= 1) # make sure it didn't match to multiple domains, which shouldn't happen
            # if it didn't match to any domain I add it to the "[Other]" domain
            if cnt == 0:
               clients_table[admin_email].domains[0].add_website(website_name)

    # Remove the subdomains which are websites
    for idx in clients_table:
        for domain in clients_table[idx].domains:
            domain.clean_subdomains()

    # put the domain "[Other]" at the end
    for idx in clients_table:
        client = clients_table[idx]
        client.domains[0], client.domains[-1] = client.domains[-1], client.domains[0]

    # return the table as a list and not as a dictionary because the dictionary was only to make the matching easier, also returned the unmatched thigs
    return [clients_table[client] for client in clients_table], domains_not_matched, websites_not_matched

def print_matched(clients, out):
    out.writerow(("Name", "Email", "Role", "Domain", "Website", "Additional Subdomain"))

    match_table = []
    for client in clients:
        table_client = []

        for domain in client.domains:
            table_domain = []

            # create the table with the size needed
            for i in range(max(len(domain.subdomains), len(domain.websites))):
                table_domain.append(6*[""])

            # add all the subdomains to their correct places
            for i in range(len(domain.subdomains)):
                table_domain[i][5] = domain.subdomains[i]

            # add the websites to their correct places
            for i in range(len(domain.websites)):
                table_domain[i][4] = domain.websites[i]

            # if there is no subdomain nor website I still need a space to add the domain name, so I create one row if there isn't
            if len(table_domain) == 0:
                table_domain.append(6*[""])

            # put the domain name
            table_domain[0][3] = domain.name

            # add it all to the client table
            for row in table_domain:
                table_client.append(row)

        # same thing as before, I need at least one row to add the name of the client
        if len(table_client) == 0:
            table_client.append(6*[""])

        table_client[0][0] = client.name
        table_client[0][1] = client.email
        table_client[0][2] = client.role

        table_client.append(6*[""]) # I'll give a space between two clients for it to look better

        # put it all on the big table
        for row in table_client:
            match_table.append(row)

    # write the big table to csv
    for row in match_table:
        out.writerow(row)

def print_not_matched(domains, websites, out):
    domains.sort()
    websites.sort()

    out.writerow(("DOMAINS", "", ""))
    out.writerow(("","Email","Domain name"))
    last = "#"
    for email,domain in domains:
        if email == last:
            out.writerow(("", "", domain))
        else:
            out.writerow(("", email, domain))
        last = email

    out.writerow(("","",""))
    out.writerow(("WEBSITES","",""))

    last = "#"
    for email,domain in websites:
        if email == last:
            out.writerow(("", "", domain))
        else:
            out.writerow(("", email, domain))
        last = email

def main():
    # read the csv files and put them through the csv library
    with open(csv_domains, 'r') as domf, open(csv_subdomains, 'r') as subdf, open(csv_websites, 'r') as webf,\
            open(csv_clients, 'r') as clif, open(csv_matched, 'w') as matf, open(csv_not_matched, 'w') as nmatf:
        domains = csv.reader(domf); subdomains = csv.reader(subdf); websites = csv.reader(webf);
        clients = csv.reader(clif); matched = csv.writer(matf); not_matched = csv.writer(nmatf);

        # match the data
        matched_data, domains_not_matched, websites_not_matched = match_data(domains, subdomains, websites, clients)
        
        # put it into the format onto the desired csv file
        print_matched(matched_data, matched)

        # put it into the format onto the desired csv file
        print_not_matched(domains_not_matched, websites_not_matched, not_matched)

if __name__ == '__main__':
    main()
