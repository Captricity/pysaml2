def replace_retrieval_method(xmlstr):
    """
    Given an XML string, replace entries of RetrievalMethod with the referred
    content. Used to support EncryptedKey retrieval method for KeyInfo in
    encrypted assertions.
    """
    from lxml import etree
    root = etree.fromstring(xmlstr)
    ds_ns = root.nsmap.get('ds', 'http://www.w3.org/2000/09/xmldsig#')
    xenc_ns = root.nsmap.get('xenc', 'http://www.w3.org/2001/04/xmlenc#')
    retrieval_methods = root.findall('.//{{{}}}RetrievalMethod'.format(ds_ns))
    replacements = []
    for retmet in retrieval_methods:
        if (retmet.attrib['Type'] !=
                'http://www.w3.org/2001/04/xmlenc#EncryptedKey'):
            # Unsupported
            continue
        uri = retmet.attrib['URI']
        if not uri.startswith('#'):
            # Unsupported
            continue
        encrypted_key = \
            root.findall(
                './/{{{}}}EncryptedKey[@Id="{}"]'.format(xenc_ns, uri[1:]))
        if len(encrypted_key) != 1:
            # Unsupported
            continue
        replacements.append((retmet, encrypted_key[0]))
    for old, new in replacements:
        parent = old.getparent()
        parent.replace(old, new)
    return etree.tostring(root)
