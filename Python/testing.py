import schedule
import time
from bs4 import BeautifulSoup
import subprocess
import pathlib
from datetime import datetime

def run_images_and_capture_ps(images):
    try:
        # Start the images using Podman
        for image in images:
            subprocess.run(['podman', 'run', '-d', '--name', image ,image], check=True)

        # Capture the output of 'podman ps' into a variable
        ps_output = subprocess.check_output(['podman', 'ps', '-a']).decode('utf-8')

        # Print the captured 'podman ps' output
        print("Podman ps output:")
        print(ps_output)

        return ps_output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def remove_images(images):
    try:
        # Start the images using Podman
        for image in images:
            subprocess.run(['podman', 'rm', '-f', image], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def init_main(ps_output,my_table,machine=None):
    
    heading = my_table.find('thead')

    if heading==None:
        headers = ['Host','Time Deployed','Operating System','Jenkins Pipeline']
        prehead = soup.new_tag('thead')
        header_row = soup.new_tag('tr')


        for head in headers:
            header_cell = soup.new_tag('th')
            header_cell.string = head
            header_row.append(header_cell)
        prehead.append(header_row)
        my_table.append(prehead)

    prebody = soup.new_tag('tbody')

    data = [init_inner(ps_output,machine),str(datetime.now().strftime("%H:%M:%S")),'RHEL 7.9','linky-link']
    row = soup.new_tag('tr')
    
    for item in data:
        if type(item)==str:
            row_cell = soup.new_tag('td')
            row_cell.string = item
            row.append(row_cell)
        else:
            row.append(item)
        
    
    prebody.append(row)
    my_table.append(prebody)

    return my_table


def init_inner(ps_output,machine=None):
    #add pre div
    tr = soup.new_tag('tr')
    
    td = soup.new_tag('td')
    td['class'] = 'summary_info'
    
    div = soup.new_tag('div')
    div['id'] = 'hostname_'+machine
    
    p = soup.new_tag('p')
    p['class'] = 'hostname'
    p.string = "Deployment Table"
    
    div.append(p)
    td.append(div)
    

    #Add accordian div
    div_acc = soup.new_tag('div')
    div_acc['id'] = 'accordian_'+machine
    
    div_acc_c1 = soup.new_tag('div')
    div_acc_c1['class'] = "ui-accordion ui-widget ui-helper-reset"
    div_acc_c1['role'] = "tablist"

    h3 = soup.new_tag('h3')
    h3['class'] = "ui-accordion-header ui-corner-top ui-state-default ui-accordion-icons ui-accordion-header-collapsed ui-corner-all"
    h3['role'] = "tab"
    h3['id'] = "ui-id-3_"+machine
    h3['aria-controls'] = "ui-id-4"
    h3['aria-selected'] = "false"
    h3['aria-expanded'] = "false"
    h3['tabindex'] = "0"
    h3.string = machine

    div_acc_c1.append(h3)

    div_acc_c2 = soup.new_tag('div')
    div_acc_c2['class'] = "net_content ui-accordion-content ui-corner-bottom ui-helper-reset ui-widget-content"
    div_acc_c2['role'] = "tabpanel"
    div_acc_c2['id'] = "ui-id-4_"+machine
    div_acc_c2['aria-labelledby'] = "ui-id-3"
    div_acc_c2['aria-hidden'] = "true"
    div_acc_c2['style'] = "display: none; height: 194px;"

    headers = ['Container ID','Image','Status','Name']
    header_row = soup.new_tag('tr')
    for head in headers:
        header_cell = soup.new_tag('th')
        header_cell.string = head
        header_row.append(header_cell)

    inner_table = soup.new_tag('table')
    thead =  soup.new_tag('thead')
    thead.append(header_row)

    inner_table.append(thead)
    inner_table['id'] = machine
    inner_table['class'] = 'sortable'

    tbody =  soup.new_tag('tbody')

    
    # Iterate through the output lines and skip the header
    for line in ps_output.split('\n')[1:]:
        if line:
            # Split the line into columns
            columns = line.split()

            # data = {container_id:columns[0],image:columns[1],command:columns[2],names:columns[-1]}
            
            # Choose columns
            data = [columns[0],columns[1],columns[2],columns[-1]]
            row = soup.new_tag('tr')
            for item in data:
                row_cell = soup.new_tag('td')
                row_cell.string = item
                row.append(row_cell)

            tbody.append(row)

    inner_table.append(tbody)
    
    div_acc_c2.append(inner_table)
    div_acc_c1.append(div_acc_c2)
    div_acc.append(div_acc_c1)

    
    td.append(div_acc)
    tr.append(td)

    return td

def update_inner(ps_output,my_table):
    
    headers = ['Container ID','Image','Status','Name']
    header_row = soup.new_tag('tr')
    for head in headers:
        header_cell = soup.new_tag('th')
        header_cell.string = head
        header_row.append(header_cell)

    tbody =  soup.new_tag('tbody')

    
    # Iterate through the output lines and skip the header
    for line in ps_output.split('\n')[1:]:
        if line:
            # Split the line into columns
            columns = line.split()

            # data = {container_id:columns[0],image:columns[1],command:columns[2],names:columns[-1]}
            
            # Choose columns
            data = [columns[0],columns[1],columns[2],columns[-1]]
            row = soup.new_tag('tr')
            for item in data:
                row_cell = soup.new_tag('td')
                row_cell.string = item
                row.append(row_cell)

            tbody.append(row)

    my_table.append(tbody)
    

    return my_table

def new_page():
    html_table = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv='refresh' content='5'>
    <style>
        p.hostname {
            color: #000000;
            font-weight: bolder;
            font-size: large;
            margin: auto;
            width: 50%;
        }
        
        #subtable {
            background: #ebebeb;
            margin: 0px;
            width: 100%;
        }
        
        #subtable tbody tr td {
            padding: 5px 5px 5px 5px;
        }
        
        #subtable thead th {
            padding: 5px;
        }
        
        * {
            -moz-box-sizing: border-box;
            -webkit-box-sizing: border-box;
            box-sizing: border-box;
            font-family: "Open Sans", "Helvetica";
        
        }
        
        a {
            color: #ffffff;
        }
        
        p {
            color: #ffffff;
        }
        h1 {
            text-align: center;
            color: #ffffff;
        }
        
        body {
            background:#353a40;
            padding: 0px;
            margin: 0px;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        
        table {
            border-collapse: separate;
            background:#fff;
            @include border-radius(5px);
            @include box-shadow(0px 0px 5px rgba(0,0,0,0.3));
        }

        .main_net_table {
            margin:50px auto;
        }
        
        thead {
            @include border-radius(5px);
        }
        
        thead th {
            font-size:16px;
            font-weight:400;
            color:#fff;
            @include text-shadow(1px 1px 0px rgba(0,0,0,0.5));
            text-align:left;
            padding:20px;
            border-top:1px solid #858d99;
            background: #353a40;
        
            &:first-child {
            @include border-top-left-radius(5px);
            }
        
            &:last-child {
            @include border-top-right-radius(5px);
            }
        }
        
        tbody tr td {
            font-weight:400;
            color:#5f6062;
            font-size:13px;
            padding:20px 20px 20px 20px;
            border-bottom:1px solid #e0e0e0;
        }
        
        tbody tr:nth-child(2n) {
            background:#f0f3f5;
        }
        
        tbody tr:last-child td {
            border-bottom:none;
            &:first-child {
            @include border-bottom-left-radius(5px);
            }
            &:last-child {
            @include border-bottom-right-radius(5px);
            }
        }
        
        td {
            vertical-align: top;
        }

        span.highlight {
            background-color: yellow;
        }
        
        .expandclass {
            color: #5f6062;
        }
        
        .content{
                display:none;
                margin: 10px;
        }
        
        header {
            width: 100%;
            position: initial;
            float: initial;
            padding: 0;
            margin: 0;
            border-radius: 0;
            height: 88px;
            background-color: #171717;
        }
        
        .header-container {
            margin: 0 auto;
            width: 100%;
            height: 100%;
            max-width: 1170px;
            padding: 0;
            float: initial;
            display: flex;
            align-items: center;
        }
        
        .header-logo {
            width: 137px;
            border: 0;
            margin: 0;
            margin-left: 15px;
        }
        
        .header-link {
            margin-left: 40px;
            text-decoration: none;
            cursor: pointer;
            text-transform: uppercase;
            font-size: 15px;
            font-family: 'Red Hat Text';
            font-weight: 500;
        }
        
        .header-link:hover {
            text-shadow: 0 0 0.02px white;
            text-decoration: none;
        }
        
        table.net_info td {
            padding: 5px;
        }

        p.expandclass:hover {
            text-decoration: underline;
            color: #EE0000;
            cursor: pointer;
        }

        .summary_info {
        }

        .ui-state-active, .ui-widget-content .ui-state-active, .ui-widget-header .ui-state-active, a.ui-button:active, .ui-button:active, .ui-button.ui-state-active:hover {
            border: 1px solid #5F0000;
            background: #EE0000;
        }

        div#net_content {
            padding: 0px;
            height: auto !important;
        }

        img.router_image {
            vertical-align: middle;
            padding: 0px 10px 10px 10px;
            width: 50px;
        }

        table.net_info {
            width: 100%;
        }

        p.internal_label {
            color: #000000;
        }
    </style>
    <script>
    $(function() {
    $( "#accordion > div" ).accordion({
        header: "h3",
        active: false,
    collapsible: true
    });
    });
    </script>
    <script>
        (function(document) {
            'use strict';

            var TableFilter = (function(myArray) {
                var search_input;

                function _onInputSearch(e) {
                    search_input = e.target;
                    var tables = document.getElementsByClassName(search_input.getAttribute('data-table'));
                    myArray.forEach.call(tables, function(table) {
                        myArray.forEach.call(table.tBodies, function(tbody) {
                            myArray.forEach.call(tbody.rows, function(row) {
                                var text_content = row.textContent.toLowerCase();
                                var search_val = search_input.value.toLowerCase();
                                row.style.display = text_content.indexOf(search_val) > -1 ? '' : 'none';
                            });
                        });
                    });
                }

                return {
                    init: function() {
                        var inputs = document.getElementsByClassName('search-input');
                        myArray.forEach.call(inputs, function(input) {
                            input.oninput = _onInputSearch;
                        });
                    }
                };
            })(Array.prototype);

            document.addEventListener('readystatechange', function() {
                if (document.readyState === 'complete') {
                    TableFilter.init();
                }
            });

        })(document);
    </script>
    </head>
    <body>
        <div class="wrapper">
            <header>
            <div class="header-container">
                <a href="https://ansible.com">
                <img
                    class="header-logo"
                    src="redhat-ansible-logo.svg"
                    title="Red Hat Ansible"
                    alt="Red Hat Ansible"
                />
                </a>
            </div>
            </header>
        <section>
        <center>
            <h1>Deployment Automation Report</h1>
            <h3><input type="search" placeholder="Search..." class="form-control search-input" data-table="main_net_table"/>
        </center>
        <table id="main" class="table table-striped mt32 main_net_table">
        </table>
        </section>
        </div>
    </body>
    </html>
    """

    with open('container_table.html', 'w', encoding='utf-8') as file:
        file.write(html_table)

# Example usage
if __name__ == "__main__":
    images2 = ["alpine", "busybox", "python"]
    images1 = ["redis", "golang", "ubuntu"]

    ps_output = run_images_and_capture_ps(images1)

     # Initialize an HTML table with CSS styling
    if pathlib.Path(pathlib.Path.cwd() / 'container_table.html').exists():
        pass
    else:
        new_page()

    if ps_output:
        # Read the HTML content from a local file
        with open(pathlib.Path.cwd() / 'container_table.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the table element you want to update, e.g., by its ID or class
        table = soup.find('table', id='machine-01')

        if table:
            for row in table.find_all('tr'):
                if row.find('td') or row.find('th'):
                    row.extract()
            
            table = update_inner(ps_output,my_table=table)
        else:
            table = init_main(ps_output,my_table=soup.find('table', id='main'),machine='machine-01')

            soup.body.append(table)

        # parent_tag = table.find_parent()
        # br_tag = soup.new_tag('br')
        # parent_tag.append(br_tag)
        # parent_tag.append(br_tag)
        # parent_tag.append(br_tag)
        
        # Save the updated HTML content back to the local file
        with open(pathlib.Path.cwd() / 'container_table.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())  
            
            
        print("HTML table has been generated in 'container_table.html'")
        time.sleep(5)
        remove_images(images1)
        time.sleep(5)
        pass
    else:
        print("Failed to run containers or capture 'podman ps' output.")


    
    ps_output = run_images_and_capture_ps(images2)

    if ps_output:
        # Read the HTML content from a local file
        with open(pathlib.Path.cwd() / 'container_table.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the table element you want to update, e.g., by its ID or class
        table = soup.find('table', id='machine-02')

        if table:
            for row in table.find_all('tr'):
                if row.find('td') or row.find('th'):
                    row.extract()
            
            table = update_inner(ps_output,my_table=table)
        else:
            table = init_main(ps_output,my_table=soup.find('table', id='main'),machine='machine-02')
            
            soup.body.append(table)

        # parent_tag = table.find_parent()
        # br_tag = soup.new_tag('br')
        # parent_tag.append(br_tag)
        # parent_tag.append(br_tag)
        # parent_tag.append(br_tag)

        # Save the updated HTML content back to the local file
        with open(pathlib.Path.cwd() / 'container_table.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())           

        print("HTML table has been generated in 'container_table.html'")
        time.sleep(5)
        remove_images(images2)
        time.sleep(5)
        pass
    else:
        print("Failed to run containers or capture 'podman ps' output.")
