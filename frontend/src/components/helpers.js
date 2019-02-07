export function urlEncode (obj) {
  return Object.keys(obj).reduce(function (a, k) {
    a.push(k + '=' + encodeURIComponent(obj[k]))
    return a
  }, []).join('&')
}

export function formatLabel (str, maxwidth) {
  if (str === null || str === '') {
    return []
  }
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

export function formatDate (date, short) {
  return ('0' + date.getDate()).slice(-2) +
    '.' + ('0' + (date.getMonth() + 1)).slice(-2) +
    (short === undefined ? ('.' + date.getFullYear()) : '')
}

export function deltaToHMM (delta) {
  var hours = Math.floor(delta)
  var minutes = Math.floor((delta - hours) * 60)

  if (minutes < 10) {
    minutes = '0' + minutes
  }

  return hours + ':' + minutes
}

export default {urlEncode, formatLabel, formatDate, deltaToHMM}
