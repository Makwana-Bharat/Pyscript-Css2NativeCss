import cssutils
import json
import re


def css_to_json(css_code):
    # Create a CSSParser instance
    parser = cssutils.CSSParser()

    try:
        # Parse the CSS code
        stylesheet = parser.parseString(css_code)

        # Convert the parsed CSS data to a dictionary
        css_data = {}
        for rule in stylesheet:
            if isinstance(rule, cssutils.css.CSSStyleRule):
                selector = rule.selectorText.strip('"')  # Remove quotes
                properties = {}
                for prop in rule.style:
                    prop_name = prop.name.strip('"')  # Remove quotes
                    if (prop_name[0].upper() not in [chr(i) for i in range(65, 92)]):
                        prop_name = prop_name[1:]
                    if (len(prop_name.split("-")) == 2):
                        prop_name = prop_name.split(
                            "-")[0]+(prop_name.split("-")[1].capitalize())
                    properties[prop_name] = prop.value
                css_data[selector] = properties

        # Convert the dictionary to JSON
        json_data = json.dumps(css_data, indent=4)

        return json_data
    except cssutils.CSSException as e:
        print("")
        return None


if __name__ == "__main__":
    css_code = """
    body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 0;
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
}

h1 {
    color: #333;
    font-size: 24px;
}

p {
    color: #666;
    font-size: 16px;
    line-height: 1.5;
}
    """

    json_data = css_to_json(css_code)
    reactNativeCss = ""
    if json_data:
        reactNativeCss = "const styles = StyleSheet.create("+json_data+");"
    reactNativeCss = re.sub(r'"([^"]+)":', r'\1:', reactNativeCss)
    # Element("result").element.value = reactNativeCss
    print(reactNativeCss)
