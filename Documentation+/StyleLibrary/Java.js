window.onload = BodyOnLoad;

function BodyOnClick (e)
{
	var t;

	if (!e) var e = window.event;
	if (e.target) t = e.target;
	else if (e.srcElement) t = e.srcElement;
	if (t.nodeType == 3) // defeat Safari bug
		t = t.parentNode;

	var requirementsPopup	= document.getElementById ('requirementsPopup');
	var seeAlsoPopup		= document.getElementById ('seeAlsoPopup');

	if ((t.id == 'requirementsLink') && (seeAlsoPopup) &&
		(seeAlsoPopup.style.visibility == 'visible'))
	{
		HidePopupLayer ('seeAlsoPopup');
	} else {
		if ((t.id == 'seeAlsoLink') && (requirementsPopup) &&
			(requirementsPopup.style.visibility == 'visible'))
		{
			HidePopupLayer ('requirementsPopup');
		} else {
			if ((t.id != 'requirementsLink') && (t.id != 'seeAlsoLink')) {
				HidePopupLayer ('seeAlsoPopup');
				HidePopupLayer ('requirementsPopup');
			}
		}
	}
}

function BodyOnLoad ()
{
	DoSyntaxHighlight ();
	InitPopupLayers ();
	document.body.onclick = BodyOnClick;
	window.onresize = SetPopupLayerWidths;
}

function InitPopupLayers ()
{
	var requirements;
	var hasRequirements = false;
	var seeAlso;
	var hasSeeAlso = false;
	var i;

	var headings = document.getElementsByTagName ('h4');
	var headingCount = headings.length;

	for (i = 0; i < headingCount; i++) {
		if (headings[i].innerHTML.match (/^[\s\r\n]*Requirements[\s\r\n]*$/)) {
			requirements = headings[i];
			hasRequirements = true;
		}
		if (headings[i].innerHTML.match (/^[\s\r\n]*See[\s\r\n]+Also[\s\r\n]*$/)) {
			seeAlso = headings[i];
			hasSeeAlso = true;
		}
		if (hasRequirements && hasSeeAlso) {
			break;
		}
	}
	if (!hasSeeAlso || !hasRequirements) {
		var headings = document.getElementsByTagName ('h3');
		var headingCount = headings.length;

		for (i = 0; i < headingCount; i++) {
			if (!hasRequirements && (headings[i].innerHTML.match (/^[\s\r\n]*Requirements[\s\r\n]*$/))) {
				requirements = headings[i];
				hasRequirements = true;
			}
			if (!hasSeeAlso && (headings[i].innerHTML.match (/^[\s\r\n]*See[\s\r\n]+Also[\s\r\n]*$/))) {
				seeAlso = headings[i];
				hasSeeAlso = true;
			}
			if (hasRequirements && hasSeeAlso) {
				break;
			}
		}
	}
	if (!hasSeeAlso || !hasRequirements) {
		var headings = document.getElementsByTagName ('h2');
		var headingCount = headings.length;

		for (i = 0; i < headingCount; i++) {
			if (!hasRequirements && (headings[i].innerHTML.match (/^[\s\r\n]*Requirements[\s\r\n]*$/))) {
				requirements = headings[i];
				hasRequirements = true;
			}
			if (!hasSeeAlso && (headings[i].innerHTML.match (/^[\s\r\n]*See[\s\r\n]+Also[\s\r\n]*$/))) {
				seeAlso = headings[i];
				hasSeeAlso = true;
			}
			if (hasRequirements && hasSeeAlso) {
				break;
			}
		}
	}
	if (!hasSeeAlso || !hasRequirements) {
		var headings = document.getElementsByTagName ('h1');
		var headingCount = headings.length;

		for (i = 0; i < headingCount; i++) {
			if (!hasRequirements && (headings[i].innerHTML.match (/^[\s\r\n]*Requirements[\s\r\n]*$/))) {
				requirements = headings[i];
				hasRequirements = true;
			}
			if (!hasSeeAlso && (headings[i].innerHTML.match (/^[\s\r\n]*See[\s\r\n]+Also[\s\r\n]*$/))) {
				seeAlso = headings[i];
				hasSeeAlso = true;
			}
			if (hasRequirements && hasSeeAlso) {
				break;
			}
		}
	}

	var styleLibraryLocation	= document.getElementById ('toTopImg').src.replace (/top.png$/, '');
	styleLibraryLocation	= styleLibraryLocation.replace (/top.gif$/, '');
	var requirementsImage;
	var seeAlsoImage;

	if (hasRequirements) {
		var requirementsDiv = document.createElement ('div');
		requirementsDiv.appendChild (requirements.cloneNode (true));

		var requirementsNode = requirements.nextSibling; 
		var requirementsNodeName = requirementsNode.nodeName.toLowerCase ();

		while ( (requirementsNode) &&
				(requirementsNodeName != 'h1') &&
				(requirementsNodeName != 'h2') &&
				(requirementsNodeName != 'h3') &&
				(requirementsNodeName != 'h4') &&
				(requirementsNodeName != 'table') &&
				(requirementsNodeName != 'div')
			  )
		{
			requirementsDiv.appendChild (requirementsNode.cloneNode (true));
			requirementsNode = requirementsNode.nextSibling;

			if (requirementsNode) {
				requirementsNodeName = requirementsNode.nodeName.toLowerCase ();
			}
		}

		requirementsDiv.className = 'Popup';
		requirementsDiv.setAttribute ('id', 'requirementsPopup');
		requirementsImage = document.createElement ('img');
		requirementsImage.setAttribute ('id', 'requirementsLink');
		requirementsImage.setAttribute ('src', styleLibraryLocation + 'requirements.png');
		requirementsImage.onclick = new Function ("ShowPopupLayer ('requirementsPopup')");
	}

	if (hasSeeAlso) {
		var seeAlsoDiv = document.createElement ('div');
		seeAlsoDiv.appendChild (seeAlso.cloneNode (true));

		var seeAlsoNode = seeAlso.nextSibling; 
		var seeAlsoNodeName = seeAlsoNode.nodeName.toLowerCase ();

		while ( (seeAlsoNode) &&
				(seeAlsoNodeName != 'h1') &&
				(seeAlsoNodeName != 'h2') &&
				(seeAlsoNodeName != 'h3') &&
				(seeAlsoNodeName != 'h4') &&
				(seeAlsoNodeName != 'table') &&
				(seeAlsoNodeName != 'div')
			  )
		{
			seeAlsoDiv.appendChild (seeAlsoNode.cloneNode (true));
			seeAlsoNode = seeAlsoNode.nextSibling;

			if (seeAlsoNode) {
				seeAlsoNodeName = seeAlsoNode.nodeName.toLowerCase ();
			}
		}

		seeAlsoDiv.className = 'Popup';
		seeAlsoDiv.setAttribute ('id', 'seeAlsoPopup');
		seeAlsoImage = document.createElement ('img');
		seeAlsoImage.setAttribute ('id', 'seeAlsoLink');
		seeAlsoImage.setAttribute ('src', styleLibraryLocation + 'seealso.png');
		seeAlsoImage.onclick = new Function ("ShowPopupLayer ('seeAlsoPopup')");
	}
	
	var header = document.getElementById ('docBegin');
	if (hasRequirements) {
		header.insertBefore (requirementsDiv, header.firstChild);
		header.insertBefore (requirementsImage, header.firstChild);
	}
	if (hasSeeAlso) {
		header.insertBefore (seeAlsoDiv, header.firstChild);
		header.insertBefore (seeAlsoImage, header.firstChild);
	}

	SetPopupLayerWidths ();
}

function ShowPopupLayer (elementId)
{
	document.getElementById (elementId).style.visibility = 'visible';
}

function HidePopupLayer (elementId)
{
	var popupLayer = document.getElementById (elementId);
	if (popupLayer) {
		popupLayer.style.visibility = 'hidden';
	}
}

function SetPopupLayerWidths ()
{
	var popupWidth			= document.body.offsetWidth - 90 + 'px';
	var requirementsPopup	= document.getElementById ('requirementsPopup');
	var seeAlsoPopup		= document.getElementById ('seeAlsoPopup');

	if (requirementsPopup) {
		requirementsPopup.style.width = popupWidth;
	}
	if (seeAlsoPopup) {
		seeAlsoPopup.style.width = popupWidth;
	}
}

function DoSyntaxHighlight ()
{
	var preElements = document.getElementsByTagName ('pre');
	var preCount = preElements.length;
	var i = 0;

	for (i = 0; i < preCount; i++) {
		if ((preElements[i].className == 'code') || preElements[i].className == 'Code') {
			var oldCode;
			var newCode = new Array();
			if (preElements[i].outerHTML) {
				oldCode = preElements[i].outerHTML;
			} else {
				oldCode = preElements[i].innerHTML;
			}

			var j = 0;
			while (j < oldCode.length) {
				var token = "";
				var nextChar = oldCode.charAt (j);

				// skip HTML tags

				if (nextChar == '<') {
					while (j < oldCode.length && oldCode.charAt (j) != '>') {
						token += oldCode.charAt (j);
						j++;
					}
					if (j < oldCode.length) {
						token += oldCode.charAt (j);
						j++;
					}
					newCode.push (token);
				}

				// single line comments

				else if (nextChar == '/' && j + 1 < oldCode.length && oldCode.charAt (j + 1) == '/') {
					while (j < oldCode.length && oldCode.charAt (j) != '\n') {
						token += oldCode.charAt (j);
						j++;
					}
					newCode.push ('<span class="HighlightComment">' + token + '</span>');
					j++;
				}

				// multi line comments

				else if (nextChar == '/' && j + 1 < oldCode.length && oldCode.charAt (j + 1) == '*') {
					token += oldCode.charAt (j);
					token += oldCode.charAt (j + 1);
					j += 2;
					while (j + 1 < oldCode.length && !(oldCode.charAt (j) == '*' && oldCode.charAt (j + 1) == '/')) {
						token += oldCode.charAt (j);
						j++;
					}
					if (j < oldCode.length) {
						token += oldCode.charAt (j);
						j++;
					}
					if (j < oldCode.length) {
						token += oldCode.charAt (j);
						j++;
					}
					newCode.push ('<span class="HighlightComment">' + token + '</span>');
				}

				// strings

				else if (nextChar == '"' && j > 0 && oldCode.charAt (j - 1) != '\\') {
					token += nextChar;
					j++;
					while (j < oldCode.length && oldCode.charAt (j) != '"' && oldCode.charAt (j) != '\n') {
						if (j + 1 < oldCode.length && oldCode.charAt (j) == '\\' && oldCode.charAt (j + 1) == '"') {
							token += oldCode.charAt (j);
							j++;	
						}
						token += oldCode.charAt (j);
						j++;
					}
					if (j < oldCode.length && oldCode.charAt (j) == '"') {
						token += oldCode.charAt (j);
						j++;
						newCode.push ('<span class="HighlightString">' + token + '</span>');
					} else {
						newCode.push (token);
					}
				}

				// C++ keywords

				else if (IsIdFirst (oldCode.charAt (j))) {
					token += nextChar;
					j++;
					while (j < oldCode.length && (IsIdRest (oldCode.charAt (j)))) {
						token += oldCode.charAt (j);
						j++;
					}
					if (token == "and"       || token == "and_eq"   || token == "asm"              ||
						token == "auto"      || token == "bitand"   || token == "bitor"            ||
						token == "bool"      || token == "break"    || token == "case"             ||
						token == "catch"     || token == "char"     || token == "class"            ||
						token == "compl"     || token == "const"    || token == "const_cast"       ||
						token == "continue"  || token == "default"  || token == "delete"           ||
						token == "do"        || token == "double"   || token == "dynamic_cast"     ||
						token == "else"      || token == "enum"     || token == "explicit"         ||
						token == "export"    || token == "extern"   || token == "false"            ||
						token == "float"     || token == "for"      || token == "friend"           ||
						token == "goto"      || token == "if"       || token == "inline"           ||
						token == "int"       || token == "long"     || token == "mutable"          ||
						token == "namespace" || token == "new"      || token == "not"              ||
						token == "not_eq"    || token == "operator" || token == "or"               ||
						token == "or_eq"     || token == "private"  || token == "protected"        ||
						token == "public"    || token == "register" || token == "reinterpret_cast" ||
						token == "return"    || token == "short"    || token == "signed"           ||
						token == "sizeof"    || token == "static"   || token == "static_cast"      ||
						token == "struct"    || token == "switch"   || token == "template"         ||
						token == "this"      || token == "throw"    || token == "true"             ||
						token == "try"       || token == "typedef"  || token == "typeid"           ||
						token == "typename"  || token == "union"    || token == "unsigned"         ||
						token == "using"     || token == "virtual"  || token == "void"             ||
						token == "volatile"  || token == "wchar_t"  || token == "while"            ||
						token == "xor"       || token == "xor_eqt")
					{
						newCode.push ('<span class="HighlightKeyword">' + token + '</span>');
					} else {
						newCode.push (token);
					}
				}

				// preprocessor directives

				else if (nextChar == '#' && j + 1 < oldCode.length) {
					token += nextChar;
					j++;
					while (j < oldCode.length && (IsIdRest (oldCode.charAt (j)))) {
						token += oldCode.charAt (j);
						j++;
					}
					if (token == "#define" || token == "#elif"	 || token == "#else"    ||
						token == "#endif"  || token == "#error"	 || token == "#if"	    ||
						token == "#ifdef"  || token == "#ifndef" || token == "#include" ||
						token == "#line"   || token == "#pragma" ||	token == "#undef")
					{
						newCode.push ('<span class="HighlightPreprocessor">' + token + '</span>');
					} else {
						newCode.push (token);
					}
				}

				// other characters

				else {
					newCode.push (oldCode.charAt (j));
					j++;
				}
			}

			if (preElements[i].outerHTML) {
				preElements[i].outerHTML = newCode.join ('');
			} else {
				preElements[i].innerHTML = newCode.join ('');
			}
		}
	}
}

function IsLetter (ch)
{
	return ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'));
}


function IsDigit (ch)
{
	return (ch >= '0' && ch <= '9');
}


function IsIdFirst (ch)
{
	return (IsLetter (ch) || ch == '_');
}


function IsIdRest (ch)
{
	return (IsLetter (ch) || IsDigit (ch) || ch == '_');
}
