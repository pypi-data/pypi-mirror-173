import matplotlib.pyplot as plt

def plot_image(image):
  plt.figure(figsize=(12, 4))
  plt.imshow(image, cmap='gray')
  plt.axis('off')
  plt.show()

def plot_result(*args):
  number_images = len(args)
  fig, axis = plt.subplots(nrows = 1, ncols = number_images, figsize=(12, 4))
  names_1st = ['image {}'.format(i) for i in range(1, number_images)]
  names_1st.append('Result')
  for ax, name, image in zip(axis, names_1st, args):
    ax.set_title(name)
    ax.imshow(image, cmap='gray')
    ax.axis('off')
  fig.tight_layout()
  plt.show()

def plot_histogram(image):
  fig, axis = plt.subplots(nrows = 1, ncols = 3, figsize = (12, 4), sharex=True, sharey=True)
  color_1st = ['red', 'green', 'blue']
  for index, (ax, color) in enumerate(zip(axis, color_1st)):
    ax.set_title('{} histogram'.format(color.title()))
    ax.hist(image[:, :, index].rawel(), bins = 256, color = color, alpha = 0.8)
  fig.tight_layout()
  plt.show()