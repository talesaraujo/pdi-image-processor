import { api } from './api'

export function imageUpload(img) {
    let data = new FormData()

    data.append('image_file', img, img.name)

    api.post(
        '/image',
        data,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
    )
    .then((response) => console.log(response))
    .catch((error) => console.log(error))
}
