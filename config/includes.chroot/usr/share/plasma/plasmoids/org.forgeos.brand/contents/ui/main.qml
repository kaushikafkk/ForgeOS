import QtQuick 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.20 as Kirigami
import org.kde.plasma.components 3.0 as PlasmaComponents3
import org.kde.plasma.plasmoid 2.0

PlasmoidItem {
    Plasmoid.icon: "forgeos"
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation

    Plasmoid.fullRepresentation: RowLayout {
        spacing: 10
        Layout.minimumWidth: 180
        Layout.preferredWidth: 200
        Layout.fillHeight: true

        Kirigami.Icon {
            source: "forgeos"
            Layout.preferredWidth: 31
            Layout.preferredHeight: 31
        }
        PlasmaComponents3.Label {
            text: "Forge"
            color: "#f4f7f9"
            font.pixelSize: 21
            font.weight: Font.Bold
        }
        PlasmaComponents3.Label {
            text: "OS"
            color: "#ffab32"
            font.pixelSize: 21
            font.weight: Font.Bold
            Layout.leftMargin: -10
        }
    }
}
