# Performance Report Style

`perfreport.sty` provides a LaTeX package giving styling for
performance reports with SA2C branding.

## Compiling

Copy the `Makefile` into a directory containing the `.tex` file you
plan to compile. If it is not in this repository then you will need to
adjust the `PACKAGE_ROOT` variable to point to the directory
containing this `README.md`.

To compile a file named `MYTEXFILE.tex`, run:

    make MYTEXFILE.pdf

This will automatically call `latexmk` with the correct environemnt
variables and flags to compile the document.

To remove temp files, use:

    make clean-temp

To remove all generated files, use:

    make clean


## Writing LaTeX

Please write LaTeX as cleanly as possible; the style should handle the
formatting. If you find yourself having to format things by hand, then
talk to Ed so that the style file can be edited to provide the
functionality needed.

### Preamble

It *should* be sufficient to start the document as:

   \documentclass[a4paper, 11pt]{article}
    \usepackage{perfreport}

    \begin{document}

### Title page

Set parameters for the title page with `\projectname`, `\projectid`,
`\projectowner`, `\softwarename`, and `\rse`, then use `\maketitle` to
create the title page.

### Tooling information

Use the `testdetails` environment to list details of the cluster,
compiler version etc. used for testing. This creates a `tabularx`
environment. For each row of this, use a `\testdetail`, as:

    \testdetail{Name of thing}{Details about thing}

### Code listings

The `codelisting` environment is a wrapper around
`lstlisting`. Example:

    \begin{codelisting}[fontsize=8,language=fortran,caption=Some nice code]

### Function and variable names

When referring to names from the code, use
`\texttt{name}` or `\verb|name_with_bad_characters|`.

### Names of other tools

You may want to put names of other tools in **bold**.
