function toggleRows(category){
    //Tıklanan kategoriye ait tüm satırları seçme işlemi
    const rows = document.querySelectorAll('.' + category);

    rows.forEach(row => {
        //classList.contains() -> belirli css sınıfına sahip olup olmadığını kontrol eden method
        if (row.classList.contains('hidden-row')) {
            row.classList.remove('hidden-row'); // Gizliyse göster
            row.classList.add('visible-row');
        } else {
            row.classList.remove('visible-row'); // Görünürse gizle
            row.classList.add('hidden-row');
        }
    });
}


