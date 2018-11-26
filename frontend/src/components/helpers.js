export function urlEncode (obj) {
  return Object.keys(obj).reduce(function (a, k) { a.push(k + '=' + encodeURIComponent(obj[k])); return a }, []).join('&')
}

export function formatLabel (str, maxwidth) {
  var sections = []
  var words = str.split(' ')
  var temp = ' '

  words.forEach(function (item, index) {
    if (temp.length > 0) {
      var concat = temp + ' ' + item
      if (concat.length > maxwidth) {
        sections.push(temp)
        temp = ''
      } else {
        if (index === (words.length - 1)) {
          sections.push(concat)
          return
        } else {
          temp = concat
          return
        }
      }
    }

    if (index === (words.length - 1)) {
      sections.push(item)
      return
    }

    if (item.length < maxwidth) {
      temp = item
    } else {
      sections.push(item)
    }
  })
  return sections
}

export default {urlEncode, formatLabel}
