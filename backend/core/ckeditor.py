custom_color_palette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]
custom_colors = [
    {
        "color": 'hsl(0, 0%, 0%)',
        "label": 'Black'
    },
    {
        "color": 'hsl(0, 0%, 30%)',
        "label": 'Dim grey'
    },
    {
        "color": 'hsl(0, 0%, 60%)',
        "label": 'Grey'
    },
    {
        "color": 'hsl(0, 0%, 90%)',
        "label": 'Light grey'
    },
    {
        "color": 'hsl(0, 0%, 100%)',
        "label": 'White',
        "hasBorder": True
    },
    {
        "color": 'hsl(0, 75%, 60%)',
        "label": 'Red'
    },
    {
        "color": 'hsl(30, 75%, 60%)',
        "label": 'Orange'
    },
    {
        "color": 'hsl(60, 75%, 60%)',
        "label": 'Yellow'
    },
    {
        "color": 'hsl(90, 75%, 60%)',
        "label": 'Light green'
    },
    {
        "color": 'hsl(120, 75%, 60%)',
        "label": 'Green'
    },
    {
        "color": 'hsl(150, 75%, 60%)',
        "label": 'Aquamarine'
    },
    {
        "color": 'hsl(180, 75%, 60%)',
        "label": 'Turquoise'
    },
    {
        "color": 'hsl(210, 75%, 60%)',
        "label": 'Light blue'
    },
    {
        "color": 'hsl(240, 75%, 60%)',
        "label": 'Blue'
    },
    {
        "color": 'hsl(270, 75%, 60%)',
        "label": 'Purple'
    },
    {
        "color": 'hsl(300, 75%, 60%)',
        "label": 'Pink'
    },
    {
        "color": 'hsl(330, 75%, 60%)',
        "label": 'Magenta'
    },
    {
        "color": 'hsl(45, 75%, 60%)',
        "label": 'Gold'
    },
    {
        "color": 'hsl(75, 75%, 60%)',
        "label": 'Olive'
    },
    {
        "color": 'hsl(105, 75%, 60%)',
        "label": 'Lime'
    },
    {
        "color": 'hsl(135, 75%, 60%)',
        "label": 'Teal'
    },
    {
        "color": 'hsl(165, 75%, 60%)',
        "label": 'Cyan'
    },
    {
        "color": 'hsl(195, 75%, 60%)',
        "label": 'Sky blue'
    },
    {
        "color": 'hsl(225, 75%, 60%)',
        "label": 'Navy'
    },
    {
        "color": 'hsl(255, 75%, 60%)',
        "label": 'Indigo'
    },
    {
        "color": 'hsl(285, 75%, 60%)',
        "label": 'Violet'
    },
    {
        "color": 'hsl(315, 75%, 60%)',
        "label": 'Rose'
    },
    {
        "color": 'hsl(15, 75%, 60%)',
        "label": 'Sunset'
    },
    {
        "color": 'hsl(135, 90%, 60%)',
        "label": 'Bright Cyan'
    },
    {
        "color": 'hsl(270, 40%, 60%)',
        "label": 'Pastel Purple'
    },
    {
        "color": 'hsl(60, 90%, 60%)',
        "label": 'Intense Yellow'
    },
    {
        "color": 'hsl(90, 60%, 60%)',
        "label": 'Lemon'
    },
    {
        "color": 'hsl(210, 40%, 60%)',
        "label": 'Powder Blue'
    },
    {
        "color": 'hsl(120, 60%, 60%)',
        "label": 'Emerald'
    },
    {
        "color": 'hsl(30, 60%, 60%)',
        "label": 'Vivid Orange'
    },
    {
        "color": 'hsl(225, 50%, 60%)',
        "label": 'Sky'
    },
    {
        "color": 'hsl(150, 70%, 60%)',
        "label": 'Mint'
    },
    {
        "color": 'hsl(300, 70%, 60%)',
        "label": 'Candy Pink'
    },
    {
        "color": 'hsl(330, 60%, 60%)',
        "label": 'Lavender'
    },
    {
        "color": 'hsl(180, 90%, 60%)',
        "label": 'Hot Pink'
    }
    # Add more colors as needed
]
BASE_CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "styles",
            "heading",
            "|",
            "bold",
            "italic",
            "Underline",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "alignment",
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "admin": {
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote"
        ],
        "toolbar": [
            "undo",
            "redo",
            "|",
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "alignment",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
            "|",
            "horizontalLine",

        ],
        "fontColor": {
            "colors": custom_colors
        },
        "fontBackgroundColor": {
            "colors": custom_colors
        },

        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:full",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter"
            ]
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties"
            ],
            "tableProperties": {
                "borderColors": custom_color_palette,
                "backgroundColors": custom_color_palette
            },
            "tableCellProperties": {
                "borderColors": custom_color_palette,
                "backgroundColors": custom_color_palette
            }
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph"
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1"
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2"
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3"
                },
                {
                    "model": "heading4",
                    "view": "h4",
                    "title": "Heading 4",
                    "class": "ck-heading_heading4"
                },
                {
                    "model": "heading5",
                    "view": "h5",
                    "title": "Heading 5",
                    "class": "ck-heading_heading5"
                },
                {
                    "model": "heading6",
                    "view": "h6",
                    "title": "Heading 6",
                    "class": "ck-heading_heading6"
                }
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
        "simpleUpload": {
            "uploadUrl": "/upload/"
        },
        "link": {
            "addTargetToExternalLinks": True
        },
        "extraPlugins": [
            "Essentials", "CodeBlock", "Autoformat", "Bold", "Italic", "Underline", "Strikethrough", "Code",
            "Subscript",
            "Superscript", "BlockQuote", "Heading", "Image", "ImageCaption", "ImageStyle", "ImageToolbar",
            "ImageResize", "Link", "List",
            "Paragraph", "Alignment", "Font", "PasteFromOffice", "SimpleUploadAdapter", "MediaEmbed", "RemoveFormat",
            "Table",
            "TableToolbar", "TableCaption", "TableProperties", "TableCellProperties", "Indent", "IndentBlock",
            "Highlight", "TodoList",
            "ListProperties", "SourceEditing", "GeneralHtmlSupport", "ImageInsert", "WordCount", "Mention", "Style",
            "HorizontalLine",
            "LinkImage"
        ]
    }
}
