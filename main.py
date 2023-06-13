import fitz  # https://pypi.org/project/PyMuPDF/
import wx  # https://pypi.org/project/wxPython/
import timeit
import os


# Flattens given PDF
def process_file(pdf_path, file_name, parent_path):

    # Open the PDF as a fitz object
    pdf = fitz.open(pdf_path)

    # Set zoom factor for 300 dpi
    mat = fitz.Matrix(300 / 72, 300 / 72)

    # Collect the pixmaps from the input PDF
    pixmaps = []
    for page in pdf:
        pix = page.get_pixmap(matrix=mat, colorspace="cmyk")
        pixmaps.append(pix)

    # Create an empty PDF file
    doc = fitz.open()

    # Loop through the pixmaps
    for i, pix in enumerate(pixmaps):

        # Convert the width and height in pixels to points
        ptWidth = pix.width / 300 * 72
        ptHeight = pix.height / 300 * 72

        # Add a new page and insert this pixmap
        page = doc.new_page(width=ptWidth, height=ptHeight)
        page.insert_image(page.rect, pixmap=pix)

    # Save the new PDF to file
    doc.save(os.path.join(parent_path, f"f_{file_name}.pdf"))


# Init script
if __name__ == '__main__':

    # Cross-Platform Open File Dialog via wxPython
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
    dialog = wx.FileDialog(None, 'Open', wildcard="*.pdf", style=style)

    # Files are chosen
    if (dialog.ShowModal() == wx.ID_OK):

        # Get the selected files
        pdf_file_paths = dialog.GetPaths()

        # Time the action for statistics
        total_time = 0

        # Loop selected files, extract file name, feed to process_file() routine
        for pdf_path in pdf_file_paths:

            # Time the action for statistics
            start_time = timeit.default_timer()

            parent_path = os.path.dirname(pdf_path)
            file_name = os.path.basename(pdf_path)
            file = os.path.splitext(file_name)

            # Flatten this file
            process_file(pdf_path, file[0], parent_path)

            # Time the action for statistics
            end_time = timeit.default_timer()
            duration = end_time - start_time
            total_time = total_time + duration

            print(f"Flattened {file_name} in {duration} seconds.")

        print(f"Flattened {len(pdf_file_paths)} PDF files in {total_time} seconds.")
