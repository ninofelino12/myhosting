function geodoo1(url) {
    fetch(url)
        .then(response => response.json())
        .then(jsonData => {
            // 1. Buat elemen tabel secara efisien
            const tabel = document.createElement('table');
            tabel.classList.add('o_list_table', 'table', 'table-sm', 'table-hover', 'position-relative', 'mb-0', 'o_list_table_ungrouped', 'table-striped');

            // 2. Bangun header tabel sekali
            const barisHeader = document.createElement('tr');
            for (const kunci in jsonData[0]) {
                const selHeader = document.createElement('th');
                selHeader.textContent = kunci;
                selHeader.style.width = '10px';
                barisHeader.appendChild(selHeader);
            }
            const thead = document.createElement('thead');
            thead.appendChild(barisHeader);
            tabel.appendChild(thead);

            // 3. Buat baris data secara massal
            const tbody = document.createElement('tbody');
            jsonData.forEach(item => {
                const barisData = document.createElement('tr');
                barisData.classList.add('o_data_row', 'o_row_draggable');
                item.forEach(nilai => {
                    const selData = document.createElement('td');
                    selData.classList.add('o_data_cell', 'cursor-pointer', 'o_field_cell', 'o_list_char', 'o_required_modifier');
                    selData.textContent = nilai;
                    barisData.appendChild(selData);
                });
                tbody.appendChild(barisData);
            });
            tabel.appendChild(tbody);

            // 4. Ganti konten dalam satu langkah
            document.getElementById('o_content').innerHTML = ''; // Hapus konten sebelumnya
            document.getElementById('o_content').appendChild(tabel);
        });
}
function geodoo(url) {

    fetch(url).then(response => response.json()).then(jsonData => {
        // Do something with the data
        var htmlTable = '<table class="o_list_table table table-sm table-hover position-relative mb-0 o_list_table_ungrouped table-striped">';
        htmlTable += `<thead><tr>`;
        for (const key in jsonData[0]) { htmlTable += `<th style="width:10px">${key}</th>` }
        htmlTable += `</thead></tr>`;
        for (const item of jsonData) {
            htmlTable += `<tr class="o_data_row o_row_draggable">`
            for (const key in jsonData[0]) {
                htmlTable += `<td class="o_data_cell cursor-pointer o_field_cell o_list_char o_required_modifier">${item[key]}</td>`;
            }
            htmlTable += `</tr>`;

        };
        htmlTable += `</table>`;
        document.getElementById('o_content').innerHTML = htmlTable;
    });
}