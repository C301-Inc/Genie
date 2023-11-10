export const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) return error.message
  else return String(error)
}

export const chunk = (array: any[], size: number): any[] => {
  const chunked = []
  let index = 0

  while (index < array.length) {
    //@ts-ignore
    chunked.push(array.slice(index, size + index))
    index += size
  }
  return chunked
}
