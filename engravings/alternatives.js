/* Наша альтернатива в карточке гравировки.
   Принцип (решение 18.11.2026, круг оптики и Коля Зотов): линзу клиента относим к одной из четырёх
   категорий по месту в линейке производителя и предлагаем нашу линзу этой категории.
   Таблица соответствий: страница «Прогрессивы: соответствие брендов и наша альтернатива» (круг «Оптика»).
   Правила проверяются по порядку, первое совпадение выигрывает. Нет совпадения: блок не показываем.
   Записи-правила (kind без «дизайн»: правила, схемы, материалы) пропускаются в index.html.
   no: исключения (офисные, водительские, спортивные, однофокальные и т.п.). */
window.ALT_OURS = {
  econom:  { cat: "Эконом",    name: "Hoyalux Daynamic",       logo: "alt/daynamic.svg" },
  mid:     { cat: "Мидл",      name: "Hoyalux Balansis",       logo: "alt/balansis.svg" },
  midprem: { cat: "Мидл прем", name: "Hoyalux iD LifeStyle 4", logo: "alt/lifestyle4.svg" },
  top:     { cat: "Топ",       name: "Varilux X track 2",      logo: "alt/xtrack2.svg" },
};
window.ALT_RULES = [
  /* HOYA */
  { b: "HOYA", re: /Amplitude Plus|Daynamic/i, c: "econom" },
  { b: "HOYA", re: /Balansis/i, c: "mid" },
  { b: "HOYA", re: /LifeStyle [34]/i, c: "midprem" },
  { b: "HOYA", re: /MySelf|MyStyle/i, c: "top" },
  /* Essilor */
  { b: "Essilor", re: /Essentials (Everyday|Active)/i, c: "econom" },
  { b: "Essilor", re: /Varilux (Liberty|Comfort New Edition|Comfort Glass)/i, c: "mid" },
  { b: "Essilor", re: /Varilux (Comfort Max|Physio)/i, c: "midprem" },
  { b: "Essilor", re: /Varilux (X\b|X |Xclusive|X Track|X Design|E Design|E 2)/i, c: "top" },
  /* Kodak (и старые Kodak у Signet Armolite) */
  { b: ["Kodak", "Signet Armolite"], re: /Kodak (Intro|Easy|Precise|Concise)/i, c: "econom" },
  { b: ["Kodak", "Signet Armolite"], re: /Kodak Unique/i, c: "midprem" },
  /* Nikon */
  { b: "Nikon", re: /Presio (Entry|First|Balance|i\b)/i, c: "econom" },
  { b: "Nikon", re: /Presio (Advance|W\b)|DigiLife/i, c: "mid" },
  { b: "Nikon", re: /Presio Power/i, c: "midprem" },
  { b: "Nikon", re: /SeeMax (Master|Ultimate|Power|AP)|Presio (Master|Ultimate)/i, c: "top" },
  /* ZEISS: только прогрессивы общего назначения */
  { b: "ZEISS", no: /DriveSafe|Superb Sport|Individual Sport|Plus 2 Sport|EnergizeMe|Officelens|Single Vision|S\/V|Digital|Bifocal|Trifocal/i },
  { b: "ZEISS", re: /Light 2 3D/i, c: "econom" },
  { b: "ZEISS", re: /Pure|SmartLife (Progressive )?Plus|Progressive SmartLife Plus|Progressive Plus 2|Precision Plus/i, c: "mid" },
  { b: "ZEISS", re: /Superb/i, c: "midprem" },
  { b: "ZEISS", re: /Individual/i, c: "top" },
  /* Seiko */
  { b: "Seiko", no: /Drive|Curved|Indoor|SmartZoom|Computer|монофокальн|Sportstech|INDI-SV|Tribrid White|Wing|Neo|VSX|Extensive/i },
  { b: "Seiko", re: /Vision X|Synergy/i, c: "econom" },
  { b: "Seiko", re: /Prime Xceed|I Xceed|Superior/i, c: "midprem" },
  { b: "Seiko", re: /Emblem|Prime/i, c: "mid" },
  { b: "Seiko", re: /Brilliance/i, c: "top" },
  /* Shamir */
  { b: "Shamir", no: /Driver|Attitude|Computer|WorkSpace|Smart |SV|Relax|Duo|Bifocal/i },
  { b: "Shamir", re: /Genesis|Spectrum|Millennium/i, c: "econom" },
  { b: "Shamir", re: /Urban/i, c: "mid" },
  { b: "Shamir", re: /Intelligence/i, c: "top" },
  { b: "Shamir", re: /InTouch|Autograph/i, c: "midprem" },
  /* Rodenstock */
  { b: "Rodenstock", no: /Ergo|Mono|Sport|Hyperop|Cosmolit|Perfalit|Nexyma|Impression B\.I\.G\. NORM \(.*Multigressiv/i }, /* общая гравировка трёх линз B.I.G. NORM: уровень не определить */
  { b: "Rodenstock", re: /Progressiv (Life|PureLife|life|AT)/i, c: "econom" },
  { b: "Rodenstock", re: /Progressiv B\.I\.G/i, c: "mid" },
  { b: "Rodenstock", re: /Multigressiv/i, c: "midprem" },
  { b: "Rodenstock", re: /Impression|FreeSign/i, c: "top" },
  /* Ital Lenti */
  { b: "Ital Lenti", no: /Office|Relax|Extesa|EasyDrive|4Sport|Bifo/i },
  { b: "Ital Lenti", re: /FreeLine|Sky Comfort/i, c: "econom" },
  { b: "Ital Lenti", re: /Premium Mobile|Premium Armonie|PremiumHV/i, c: "midprem" },
  { b: "Ital Lenti", re: /Premium/i, c: "mid" },
  { b: "Ital Lenti", re: /Twice/i, c: "top" },
];
