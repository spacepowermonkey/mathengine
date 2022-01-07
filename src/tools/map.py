def map(model, obj_fn, obj_acc, arr_fn, arr_acc):
    for obj in model.objects():
        obj_acc += obj_fn(obj)

    for arr in model.arrows():
        arr_acc += arr_fn(arr)

    return (obj_acc, arr_acc)
