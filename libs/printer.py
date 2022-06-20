from rich.table import Table
from rich import box
from rich import print

def print_lists(lists):
    table = Table(box=box.SIMPLE, show_header=True, header_style='bold #2070b2')
    table.add_column("", justify="right", style="green", no_wrap=True)
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="blue")
    for list in lists:
        table.add_row(':heavy_check_mark:',f'{list["name"]}', f'{list["description"]}')
    
    print(table)

def print_objects(objects):
    table = Table(box=box.SIMPLE, show_header=True, header_style='bold #2070b2')
    table.add_column("", justify="right", style="green", no_wrap=True)
    table.add_column("Title", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Attachments", style="blue")
    table.add_column("Filters", style="green")
    table.add_column("Extra Information", style="blue")
    for object in objects:
        attachments=""
        for key,value in object["attachments"].items():
            if key=="others" and len(value)<1: continue
            attachments += f'| {key} : {value} '
        
        filters=""
        for key,value in object["filters"].items():
            if key=="others" and len(value)<1: continue
            filters += f'| {key} : {value} '

        table.add_row( ':heavy_check_mark:',
                       f'{object["title"]}', 
                       f'{object["description"]}',
                       attachments,
                       filters,
                       f'{object["information"]}' )

    
    print(table)